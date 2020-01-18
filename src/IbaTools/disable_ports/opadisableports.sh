#!/bin/bash
# BEGIN_ICS_COPYRIGHT8 ****************************************
# 
# Copyright (c) 2015, Intel Corporation
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# END_ICS_COPYRIGHT8   ****************************************


# [ICS VERSION STRING: unknown]

# disable the specified set of ports


# optional override of defaults
if [ -f /etc/sysconfig/opa/opafastfabric.conf ]
then
	. /etc/sysconfig/opa/opafastfabric.conf
fi

. /opt/opa/tools/opafastfabric.conf.def

. /opt/opa/tools/ff_funcs

lidmap="$(mktemp --tmpdir lidmapXXXXXX)"
trap "rm -f $lidmap; exit 1" SIGHUP SIGTERM SIGINT
trap "rm -f $lidmap" EXIT

Usage_full()
{
	echo "Usage: opadisableports [-R] [-t portsfile] [-p ports] [reason] < disable.csv" >&2
	echo "              or" >&2
	echo "       opadisableports --help" >&2
	echo "   --help - produce full help text" >&2
	echo "   -R - do not attempt to get routes for computation of distance" >&2
	echo "        instead just disable switch port with lower LID assuming" >&2
	echo "        that will be closer to this node" >&2
	echo "   -t portsfile - file with list of local HFI ports used to access" >&2
	echo "                  fabric(s) for operation, default is $CONFIG_DIR/opa/ports" >&2
	echo "   -p ports - list of local HFI ports used to access fabric(s) for operation" >&2
	echo "              default is 1st active port" >&2
	echo "              This is specified as hfi:port" >&2
	echo "                 0:0 = 1st active port in system" >&2
	echo "                 0:y = port y within system" >&2
	echo "                 x:0 = 1st active port on HFI x" >&2
	echo "                 x:y = HFI x, port y" >&2
	echo "              The first HFI in the system is 1.  The first port on an HFI is 1." >&2
	echo "   reason - optional text description of reason ports are being disabled," >&2
	echo "            will be saved in the reason field of the output file" >&2
	echo  >&2
	echo "The disable.csv is an input file listing the links to disable.  It is of the" >&2 
	echo "form:" >&2
	echo "  NodeGUID;PortNum;NodeType;NodeDesc;NodeGUID;PortNum;NodeType;NodeDesc;Reason" >&2
	echo "For each listed link, the switch port closer to this node will be disabled." >&2
	echo "The Reason field is optional." >&2
	echo "An input file such as this can be generated by opaextractbadlinks or" >&2
	echo "opaextractsellinks." >&2
	echo >&2
	echo "Information about the links disabled (and the reason) will be saved (in same">&2
	echo "format) to an output file named $CONFIG_DIR/opa/disabled:hfi:port.csv where">&2
	echo "the hfi:port part of the file name is replaced by the HFI number and the port">&2
	echo "number being operated on (such as 0:0 or 1:2).  This CSV file can be used as">&2
        echo "input to opaenableports." >&2
	echo >&2
	echo " Environment:" >&2
	echo "   PORTS - list of ports, used in absence of -t and -p" >&2
	echo "   PORTS_FILE - file containing list of ports, used in absence of -t and -p" >&2
	echo "for example:" >&2
	echo "   opadisableports 'bad cable' < disable.csv" >&2
	echo "   opadisableports -p '1:1 1:2 2:1 2:2' 'dead servers' < disable.csv" >&2
	exit 0
}

Usage()
{
	echo "Usage: opadisableports [-R] [reason] < disable.csv" >&2
	echo "              or" >&2
	echo "       opadisableports --help" >&2
	echo "   --help - produce full help text" >&2
	echo "   -R - do not attempt to get routes for computation of distance" >&2
	echo "        instead just disable switch port with lower LID assuming" >&2
	echo "        that will be closer to this node" >&2
	echo "   reason - optional text description of reason ports are being disabled," >&2
	echo "            will be saved in the reason field of the output file" >&2
	echo  >&2
	echo "disable.csv is an input file listing the links to disable." >&2
	echo "It is of the form:" >&2
	echo "  NodeGUID;PortNum;NodeType;NodeDesc;NodeGUID;PortNum;NodeType;NodeDesc;Reason" >&2
	echo "For each listed link, the switch port closer to this node will be disabled." >&2
	echo "The Reason field is optional.">&2
	echo "An input file such as this can be generated by opaextractbadlinks or" >&2
	echo "opaextractsellinks." >&2
	echo >&2
	echo "Information about the links disabled (and the reason) will be saved (in same">&2
	echo "format) to an output file named $CONFIG_DIR/opa/disabled:hfi:port.csv where">&2
	echo "the hfi:port part of the file name is replaced by the HFI number and the port">&2
	echo "number being operated on (such as 0:0 or 1:2)." >&2
	echo >&2
	echo "for example:" >&2
	echo "   opadisableports 'bad cable' < disable.csv" >&2
	exit 2
}

if [ x"$1" = "x--help" ]
then
	Usage_full
fi

res=0
reason=
reason_csv=
use_distance=y

while getopts Rp:t: param
do
	case $param in
	R)	use_distance=n;;
	p)	export PORTS="$OPTARG";;
	t)	export PORTS_FILE="$OPTARG";;
	?)	Usage;;
	esac
done
shift $((OPTIND -1))
if [ $# -ge 1 ]
then
	reason="$1"
	reason_csv=";$1"	# add field separator
	shift
fi
if [ $# -ge 1 ]
then
	Usage
fi

check_ports_args opadisableports

lookup_lid()
{
	local nodeguid="$1"
	local portnum="$2"
	local guid port type desc lid

	grep "^$nodeguid;$portnum;" < $lidmap|while read guid port type desc lid
	do
		echo -n $lid
	done
}

get_distance()
{
	local lid=$1
	local port_opts
	local portguid

	if [ "$use_distance" = n ]
	then
		echo "0"
	else
		if [ "$port" -eq 0 ]
		then
			port_opts="-h $hfi" # default port to 1st active
		else
			port_opts="-h $hfi -p $port"
		fi

		portguid=$(eval opasaquery $port_opts -o portguid -l $lid)
		eval opasaquery $port_opts -o trace -g $portguid|grep GID|wc -l
	fi
}
	

disable_ports()
{
	if [ "$port" -eq 0 ]
	then
		port_opts="-h $hfi"	# default port to 1st active
	else
		port_opts="-h $hfi -p $port"
	fi
	suffix=":$hfi:$port"

	# generate lidmap
	/usr/sbin/opaextractlids $port_opts > $lidmap
	if [ ! -s $lidmap ]
	then
		echo "opadisableports: Unable to determine fabric lids" >&2
		rm -f $lidmap
		return 1
	fi

	disabled=0
	skipped=0
	failed=0
	IFS=';'
	while read nodeguid1 port1 type1 desc1 nodeguid2 port2 type2 desc2 rest
	do
		# For non ISLs pick the switch side, so we can reenable later
		if [ "$type1" = SW -a "$type2" != SW ]
		then
			lid=$(lookup_lid $nodeguid1 0)
			distance=$(get_distance $lid)
			echo "$distance;$lid;$nodeguid1;$port1;$type1;$desc1;$nodeguid2;$port2;$type2;$desc2;$rest"
		elif [ "$type1" != SW -a "$type2" = SW ]
		then
			lid=$(lookup_lid $nodeguid2 0)
			distance=$(get_distance $lid)
			echo "$distance;$lid;$nodeguid2;$port2;$type2;$desc2;$nodeguid1;$port1;$type1;$desc1;$rest"
		else
			# determine which side of ISL to disable
			lid1=$(lookup_lid $nodeguid1 0)
			lid2=$(lookup_lid $nodeguid2 0)
			if [ x"$lid1" != x -a x"$lid2" = x ]
			then
				# might be a re-disable case, use the LID we can still resolve
				distance=$(get_distance $lid1)
				echo "$distance;$lid1;$nodeguid1;$port1;$type1;$desc1;$nodeguid2;$port2;$type2;$desc2;$rest"
			elif [ x"$lid1" = x -a x"$lid2" != x ]
			then
				# might be a re-disable case, use the LID we can still resolve
				distance=$(get_distance $lid2)
				echo "$distance;$lid2;$nodeguid2;$port2;$type2;$desc2;$nodeguid1;$port1;$type1;$desc1;$rest"
			elif [ x"$lid1" = x -a x"$lid2" = x ]
			then
				# can't resolve
				lid=
				echo "0;;$nodeguid1;$port1;$type1;$desc1;$nodeguid2;$port2;$type2;$desc2;$rest"
			else
				distance1=$(get_distance $lid1)
				distance2=$(get_distance $lid2)
				if [ $(( $distance1 )) -lt $(( $distance2 )) ]
				then
					# pick side closer to FM
					echo "$distance1;$lid1;$nodeguid1;$port1;$type1;$desc1;$nodeguid2;$port2;$type2;$desc2;$rest"
				elif [ $(( $lid1 )) -eq $(( $lid2 )) ]
				then
					# this implies a switch is connected to itself
					# atypical config, for completeness pick lower port number
					if [ $(( $port1 )) -le $(( $port2 )) ]
					then
						echo "$distance1;$lid1;$nodeguid1;$port1;$type1;$desc1;$nodeguid2;$port2;$type2;$desc2;$rest"
					else
						echo "$distance2;$lid2;$nodeguid2;$port2;$type2;$desc2;$nodeguid1;$port1;$type1;$desc1;$rest"
					fi
				elif [ $(( $distance1 )) -eq $(( $distance2 )) ]
				then
					# two LIDs of an ISL are equal distance?
					# not expected, but for completeness, pick lower LID
					# as a tie breaker and assume it might be closer to FM
					# LID == tested above, but use -le to be paranoid
					if [ $(( $lid1 )) -le $(( $lid2 )) ]
					then
						echo "$distance1;$lid1;$nodeguid1;$port1;$type1;$desc1;$nodeguid2;$port2;$type2;$desc2;$rest"
					else
						echo "$distance2;$lid2;$nodeguid2;$port2;$type2;$desc2;$nodeguid1;$port1;$type1;$desc1;$rest"
					fi
				else
					# pick side closer to FM
					echo "$distance2;$lid2;$nodeguid2;$port2;$type2;$desc2;$nodeguid1;$port1;$type1;$desc1;$rest"
				fi
			fi
		fi
	done | if [ "$use_distance" = y ]
	then
		sort -r -n -t ';' -k 1	# do furthest from this node first
	else
		cat	# do in order of input file
	fi	|
	{
	while read distance lid guid port type desc lguid lport ltype ldesc rest
	do
		if [ x"$rest" != x ]
		then
			rest=";$rest"	# add field separator
		fi

		if [ x"$lid" = x ]
		then
			echo "Skipping link: $desc:$port -> $ldesc:$lport"
			skipped=$(( $skipped + 1))
		else
			echo "Disabling link: $desc:$port -> $ldesc:$lport"
			eval /usr/sbin/opaportconfig $port_opts -l $lid -m $port disable

			if [ $? = 0 ]
			then
				logger -p user.err "Disabled link: $desc:$port -> $ldesc:$lport due to: $reason"
				disabled=$(( $disabled + 1))
				if [ ! -e $CONFIG_DIR/opa/disabled$suffix.csv ] || ! grep "^$guid;$port;" < $CONFIG_DIR/opa/disabled$suffix.csv > /dev/null 2>&1
				then
					# keep a disabled file per local HFI:port
					# same format as our input but 1st port
					# indicates which one was disabled and
					# second port is only for info
					# if fed back into this tool will select
					# same port to disable
					echo "$guid;$port;$type;$desc;$lguid;$lport;$ltype;$ldesc$rest$reason_csv" >> $CONFIG_DIR/opa/disabled$suffix.csv
				fi
			else
				failed=$(( $failed + 1))
			fi
		fi
	done
	if [ $failed -eq 0 ]
	then
		echo "Disabled: $disabled; Skipped: $skipped"
		return 0
	else
		echo "Disabled: $disabled; Skipped: $skipped; Failed: $failed"
		return 1
	fi
	}
}


for hfi_port in $PORTS
do
	hfi=$(expr $hfi_port : '\([0-9]*\):[0-9]*')
	port=$(expr $hfi_port : '[0-9]*:\([0-9]*\)')
	/usr/sbin/oparesolvehfiport $hfi $port >/dev/null
	if [ $? -ne 0 -o "$hfi" = "" -o "$port" = "" ]
	then
		echo "opadisableports: Error: Invalid port specification: $hfi_port" >&2
		res=1
		continue
	fi

	echo "Processing fabric: $hfi:$port..."
	echo "--------------------------------------------------------"
	disable_ports "$hfi" "$port"
	if [ $? -ne 0 ]
	then
		res=1
	fi
done

exit $res
