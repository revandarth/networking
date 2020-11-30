#! /bin/bash

# USAGE: no arguments!
# Runs curl, traceroute, and ping to the websites in the list

function curlGet() {
	dest=$1			# First argument is the website
	fetchsize=$2		# Second is fetch-size
	

        flag=`echo $dest|awk '{print match($0,"https")}'`;
        if [ $flag -gt 0 ];then
            port=443;
        else
            port=80;
        fi
	
	# TCP-DUMP based data collection added here to enable loss-estimation
	killall tcpdump --quiet
	/usr/sbin/tcpdump -i eth0 -tt "tcp port $port" 2>&1 > dumpfile &
	
	# Go fetch!
	if [ $fetchsize -eq -1 ]; then
		curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36" -L --max-redirs 0 -w "@curlformat.txt" -o /dev/null -s $dest -m 60 --trace-ascii curl.trace > curllog 
	else 
		curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36" -r 0-$fetchsize -L --max-redirs 0 -w "@curlformat.txt" -o /dev/null -s $dest -m 60 --trace-ascii curl.trace > curllog
	fi

	# Condense the tcp data
	killall tcpdump --quiet
	cat dumpfile | sort -k1 | awk 'NF>1' | awk '{if(NR==1){plnode=$3; serv=substr($5, 1, length($5)-1); t0 = $1}; if ($3==serv && $8!="ack") {split($9,arr,":"); pack=($1-t0); printf("%d %d %.1f\n", arr[1], arr[2], 1000*pack)}}' > tcpdata

	rm -rf dumpfile
}

function doStuff() {
	dest=$1			# First argument is the website
	fetchsize=$2		# Second is fetch-size
	whichlog=$3

# 	doesItObeySize=`grep "$dest" noObeySize`
# 	if [ ! -z "$doesItObeySize" ]; then
# 		echo "$dest doesn't obey size"
# 		return;
# 	fi

	rm -rf curl.trace* curllog* tcpdata*

	# First fetch the URL
	curlGet $dest $fetchsize
	mv curllog curllog.cold && mv curl.trace curl.trace.cold && mv tcpdata tcpdata.cold

	# Fetch again -- HOT LOAD!!
	curlGet $dest $fetchsize

	# Get data from curl log
	destip=`cat curl.trace.cold | grep "Connected to" | head -1 | awk -F'[()]' '{print $2}'`
	destipHOT=`cat curl.trace | grep "Connected to" | head -1 | awk -F'[()]' '{print $2}'`

	echo "########################### NEW LOG BEGINS #############################################" > thisLog

	echo "DEST" $dest >> thisLog

	echo "TIME_OF_TEST" `date +%s` >> thisLog

	# Push curl data to the log
	echo "DESTIP" $destip >> thisLog
	echo "DESTIPHOT" $destipHOT >> thisLog
	cat curllog.cold >> thisLog
	echo "CURLHOT FOLLOWS" >> thisLog
	cat curllog >> thisLog
	
# 	size0=`cat thisLog | grep "size_download" | awk '{print $2}' | head -1`
# 	if [ $size0 -gt 100 -a $fetchsize -eq 0 ]; then  # Does not obey size; Record
# 		echo $dest >> noObeySize
# 	fi
	
	# << Don't want anything with redirects now
	redirects=`cat curllog.cold | grep "num_redirects" | awk '{print $2}'`
	numConn=`cat curl.trace.cold | grep "Connected to" | wc -l`
	if [ $redirects -gt 0 ]; then
		rm -rf thisLog
		return;
	fi
	if [ $numConn -gt 1 ]; then
		rm -rf thisLog
		return;
	fi
	# >>

	echo "############### START TCP-DATA"  >> thisLog
	cat tcpdata.cold >> thisLog
	echo "############### END TCP-DATA"  >> thisLog
	#cat tcpdata >> thisLog

	# Run ping to destination's IP, append to log
	echo "############### START PING"  >> thisLog
	ping -c 30 -t 30 -i 0.2 $destip >> thisLog
	echo "############### END PING"  >> thisLog

	# Run traceroute to destination's IP, and append to the log
	echo "############### START TR"  >> thisLog
	traceroute -w 1 $destip -N 16 -n >> thisLog
	echo "############### END TR"  >> thisLog
	
	echo "########################### LOG ENDS #############################################" >> thisLog

	if [ $fetchsize -eq -1 ]; then
		cat thisLog >> nativeSize_"${whichlog}".log2
	else
		cat thisLog >> "${whichlog}".log2
	fi
	rm -rf thisLog curllog* curl.tr*
}

function uploadFile()
{
    file=$1
    type=$2
    
    echo "#################### UPLOADING FILE $file #####################################"

    #creates a new file descriptor 3 that redirects to 1 (STDOUT)
    exec 3>&1 
    # Run curl in a separate command, capturing output of -w "%{http_code}" into HTTP_STATUS
    # and sending the content to this command's STDOUT with -o >(cat >&3)
    #resp=$(curl -F upfile=@$file -F type=$type -F source=$ip -w "%{http_code}" -o >(cat >&3) 'http://152.3.136.67/upload_file.php')
    if [ ${#myIp} -gt 0 ]; then
        resp=$(curl -F upfile=@$resultsDir/$file -F type=$type -F source=$myIp -w "%{http_code}" -o >(cat >&3) 'https://cgi.cs.duke.edu/cspeed/upload_file.php')
    else
        resp=$(curl -F upfile=@$resultsDir/$file -F type=$type -w "%{http_code}" -o >(cat >&3) 'https://cgi.cs.duke.edu/cspeed/upload_file.php')
    fi

    if [ $resp -ne 200 ]; then
	echo "Failed to send file $file"
	grep -q -F $file unsent || echo $file >> unsent
    fi    
}

function reSendUnsentFiles()
{
    unsentfile=$1
    
    #try to send any unsent file
    cp $unsentfile tempfile
    rm $unsentfile -rf
    touch $unsentfile
    for filetosend in `cat tempfile`
    do
	if [ "$filetosend" == "$userDataFile" ]; then
	    uploadFile $filetosend 'user_data'
	elif [[ $filetosend == *har ]]; then
	    uploadFile $filetosend 'har_file'
	else
	    uploadFile $filetosend 'test_data'
	fi
    done
    rm tempfile -rf
}

function runSpeedTest()
{
    # Run a speedtest
    echo "##################### RUNNING A SPEED TEST... #############################"
    python speedtest_cli.py | tee speed_test.txt
    echo "################### START SPEED TEST" > speed.txt
    awk '/Download:/' speed_test.txt >> speed.txt
    awk '/Upload:/' speed_test.txt >> speed.txt
    echo "################### END SPEED TEST" >> speed.txt
    rm -rf speed_test.txt
}

function getUserConsent()
{
# Select 50 websites for running the tests
awk 'NR <= 25' alexa_all.txt > alexa.txt
awk 'NR > 25' alexa_all.txt | shuf | awk 'NR <= 25' >> alexa.txt

echo '                   CONSENT ABOUT RUNNING THE EXPERIMENTS

1 - The measurement script that you will run aims to measure the latency of 
web page downloads. 50 webpages will be used for the experiments. The pages were 
selected from Alexa Top 500 list from countries in different parts of the world.
The following is the list of websites that will be used in this experiment.

' > testInfo.txt


# Fit website and description to a sinle line (80 characters)
awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' alexa.txt > sitedefs.txt
awk '{print $1}' alexa.txt > sites.txt
awk -F/ '{print $3}' sites.txt > sites_no_prot.txt
awk  '{printf("%-30s\n", $0)}' sites_no_prot.txt > sites_fixed.txt
paste sites_fixed.txt sitedefs.txt > alexa_tmp.txt
cat alexa_tmp.txt >> testInfo.txt
# Remove all temp files
rm sitedefs.txt sites.txt sites_no_prot.txt sites_fixed.txt alexa_tmp.txt -rf

echo '

2.2 - We will ask you 
  * your location (country, state, city), 
  * the type of your broadband service, 
  * download and upload speeds, 
  * the price of your Internet service, and,
  * your service provider ISP. 
  
We will also measure your download and upload speeds to investigate its effect 
on TCP transfer time and latency.  
  
Your location will enable us to compare latency measurements across different 
parts of the world. Your public IP address will be collected for this purpose 
as well. Type of your Internet service will enable us to see how different 
connection types affect latency. The price, and advertised download and upload 
speeds will help us investigate how / whether these Internet service parameters 
translate into lower latency. 

2.3 - For the measurements, the following tools/utilities will be used:

2.3.1 - tcpdump : We will use tcpdump to capture your TCP traffic while 
downloading the webpages in the above list for estimating packet loss. 
Keep in mind, we would only be looking at your traffic within this VM while 
fetching the webpages.

2.3.2 - curl : curl will be used to download the landing (opening) pages of the 
websites given above. This will enable us to break down the sources of latency 
such as time taken for name resolution(DNS), time for TCP handshake, time taken 
for TCP transfer and so on. curl also will be used to upload the collected data 
to our server.

2.3.3 - ping : We will also measure the round-trip-time(RTT) to the webservers 
hosting the webpages given above using ping.

2.3.4 - traceroute : We will run a traceroute from this VM to each Web server 
in the list. This will help us analyze the latency caused at different 
locations in the end-to-end path.

2.3.5 - PhantomJS : We will use PhantomJS headless browser to obtain HTTP 
archive (HAR) files for the landing pages of the websites given above. This 
will enable us to obtain the number of objects downloaded for each page and 
latency caused by loading each object.

2.4 - An output folder will be created to temporarily store the output files. 
Each generated file will be uploaded immediately. Generated test files are not 
deleted and you can view these after an experiment is finished. 
You DO NOT HAVE TO send any output files manually.' 

>> testInfo.txt

more testInfo.txt

echo "=====================DO YOU AGREE RUNNING THE EXPERIMENTS?======================="
echo "Enter below: 1 for Yes, or 2 for No."
select yn in "Yes" "No"; do
    case $yn in
        Yes ) break;;
        No ) exit;;
    esac
done

rm testInfo.txt -rf
awk '{print $1}' alexa.txt > alexa_top.txt
rm alexa.txt -rf
}

# this function is to be used in the main loop if HAR files are to be uploaded separately
function getHttpArchiveFile()
{
    currdest=$1
    repeat=$2
    
    # Remove protocol
    harfile=`echo $currdest | cut -d':' -f 2 | cut -c 3-`
    # Remove trailing / if exists
    harfile=${harfile%/}
    # Convert /s to _s
    harfile=${harfile//\//_}
    
    for i in `seq 1 $repeat`;
        do
	    filename=$harfile\_$i.har
	    phantomjs ./harp.js $currdest $filename
	    if [ -f $filename ]; then
		mv $filename $resultsDir
		uploadFile $filename 'har_file'
	    fi
        done    
}

function getUserData()
{
    echo "###################### GETTING USER INFORMATION #######################"
    python3 user_info.py
    if [ ${#myIp} -gt 0 ]; then
        echo "IP $myIp" >> $userDataFile
    fi
    cp $userDataFile $resultsDir
    uploadFile "$userDataFile" 'user_data'
}

function cleanUpOnUserExit()
{
    killall curl tcpdump traceroute ping --quiet

    nfile=`ls $resultsDir | wc -l`
    if [ $nfile -gt 20 ]; then
        outfile=nativeSize_50.log2
        
        if [ -f $outfile ]; then
            cat speed.txt >> $outfile
            mv $outfile $resultsDir
            uploadFile $outfile 'test_data'
        fi
    fi
    
    ./clean.sh      
}

## Main loop

trap 'cleanUpOnUserExit; exit;' INT

killall curl tcpdump traceroute ping --quiet

# Check for input files, and retrieve again if they don't exist
if [ ! -f alexa_all.txt ]; then
  wget -N https://cgi.cs.duke.edu/cspeed/alexa_all.txt
fi

if [ ! -f curlformat.txt ]; then
  wget -N https://cgi.cs.duke.edu/cspeed/curlformat.txt
fi

getUserConsent

resultsDir=`date +%s | sha256sum | base64 | head -c 16`

if [ -f unsent ]; then
    rm unsent -rf
fi
touch unsent  # file to keep track of unsent files

if [ ! -d $resultsDir ]; then
    mkdir $resultsDir
fi 

userDataFile=user_data.txt

echo 'Getting user ip...'
myIp=$(curl -s https://api.ipify.org)
echo "My public IP address is: $myIp"

# Get user info
if [ ! -f $userDataFile ]; then
    getUserData
else
    savedIp=`awk '/IP/{print $2}' $userDataFile`
    if [[ "$myIp" != "$savedIp" || ${#myIp} == 0 ]]; then
        getUserData
    fi
fi

# rm -rf noObeySize
# touch noObeySize
ntest=50

#startNum=`ls -l *.log2 | awk '{print $NF}' | grep "^[0-9]*.log2" | cut -d"." -f1 | sort -n | tail -1`
startNum=0
#startNum=`cat lastSent | grep "^[0-9]*.log2" | cut -d"." -f1 | sort -n | tail -1`
if [ -z $startNum ]; then
	startNum=0
fi
endNum=`expr $startNum + $ntest`
rm -rf nativeSize_${endNum}.log2
count=$startNum	

URLfile="alexa_top.txt"
numlines=`cat $URLfile | wc -l`
exitflag=0
numlinesMinus500=`expr $numlines - $ntest`
while true
do
	# for each fetchsize
	#for fetchsize in -1 0 8000 32000 128000
	for fetchsize in -1
	do
		# Run a speed-test
		runSpeedTest
		
		echo "=========== LOADING WEB PAGES ONE BY ONE FROM THE LIST ==========="
		
		# get next 500 lines from website list
		start=`expr $count + 1`
		if [ $start -gt $numlinesMinus500 ]; then
			end=`expr $numlines`
			exitflag=1
		else
			end=`expr $count + $ntest`
		fi
		sed -ne "${start},${end}p" $URLfile | perl -MList::Util=shuffle -e 'print shuffle <>' > currlist 
		#Again, this helps ensure that each node is working on fetches in a different order, 
		#thus making sure that one single Website doesn't get a huge volume of traffic at any given time.

		# do stuff for each website
		for currdest in `cat currlist`
		do
			
			doStuff $currdest $fetchsize $end
			getHttpArchiveFile $currdest 1
		done
		
		outfile=''
		if [ $fetchsize -eq -1 ]; then
		    outfile=nativeSize_"${end}".log2
  		else
		    outfile="${end}".log2
		fi
		
		cat speed.txt >> $outfile
		mv $outfile $resultsDir
		uploadFile $outfile 'test_data'
		
		reSendUnsentFiles unsent

	done
	
	reSendUnsentFiles unsent  
	
	count=`expr $count + $ntest`

	if [ $exitflag -gt 0 ]; then
		touch iFinishedMyTask2
		exit
	fi
done
