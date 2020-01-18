/* BEGIN_ICS_COPYRIGHT7 ****************************************

Copyright (c) 2015, Intel Corporation

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
    * Neither the name of Intel Corporation nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

** END_ICS_COPYRIGHT7   ****************************************/

/* [ICS VERSION STRING: unknown] */



#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#define _GNU_SOURCE
#include <getopt.h>

#include <iba/ibt.h>
#include <oib_utils.h>

void Usage(int exitcode)
{
	fprintf(stderr, "Usage: oparesolvehfiport hfi port\n");
	fprintf(stderr, "            or\n");
	fprintf(stderr, "       oparesolvehfiport --help\n");
	fprintf(stderr, "    hfi     - hfi, numbered 1..n, 0 = system wide port num\n");
	fprintf(stderr, "              (default is 1)\n");
	fprintf(stderr, "    port    - port, numbered 1..n, 0 = 1st active\n");
 	fprintf(stderr, "              (default is 0)\n");
	fprintf(stderr, "\n");
	fprintf(stderr, "The host and port permit a variety of selections:\n");
	fprintf(stderr, "  0 0     - 1st active port in system\n");
	fprintf(stderr, "  x 0     - 1st active port on HFI x\n");
	fprintf(stderr, "  0 y     - port y within system (irrespective of which ports are active)\n");
	fprintf(stderr, "  x y     - HFI x, port y\n");
	fprintf(stderr, "\n");
	fprintf(stderr, "Example:\n");
	fprintf(stderr, "    oparesolvehfiport 0 1\n");
	fprintf(stderr, "Output:\n");
	fprintf(stderr, "    hfi_0:1\n");
	exit(exitcode);
}

int main(int argc, char ** argv)
{
    FSTATUS             fstatus;
    uint8               hfi         = 1;
    uint8               port        = 0;
    EUI64               portGuid    = -1;
	uint32 caCount, portCount;
	char fiName[255];
	int caPort;

	if (argc > 3)
	{
		fprintf(stderr, "oparesolvehfiport: Too many arguments\n");
		Usage(2);
	}
	if (argc >= 2) {
		if (strcmp(argv[1], "--help") == 0) {
			Usage(0);
		}
		if (FSUCCESS != StringToUint8(&hfi, argv[1], NULL, 0, TRUE)) {
			fprintf(stderr, "oparesolvehfiport: Invalid HFI Number: %s\n", argv[1]);
			Usage(2);
		}
	}
	if (argc == 3) {
		if (FSUCCESS != StringToUint8(&port, argv[2], NULL, 0, TRUE)) {
			fprintf(stderr, "oparesolvehfiport: Invalid Port Number: %s\n", argv[2]);
			Usage(2);
		}
	}

	// find portGuid specified
	fstatus = oib_get_portguid(hfi, port, NULL, NULL, &portGuid, NULL, NULL,
								&caCount, &portCount, fiName, &caPort, NULL);

	if (FNOT_FOUND == fstatus) {
		fprintf(stderr, "oparesolvehfiport: %s\n",
			iba_format_get_portguid_error(hfi, port, caCount, portCount));
		return 1;
	} else if (FSUCCESS != fstatus) {
		fprintf(stderr, "opasaquery: iba_get_portguid Failed: %s\n", iba_fstatus_msg(fstatus));
		return 1;
	}
    //printf("PORT GUID 0x%016"PRIx64"\n",portGuid);

	printf("%s:%d\n", fiName, caPort);

	return 0;
}
