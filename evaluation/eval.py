#  Copyright (c) 2018 5GTANGO, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).


# script for packaging, onboarding, and instantiating NS1 and NS2 and measuring the time (over multiple runs)
import requests
from time import sleep
from timeit import default_timer as timer
from subprocess import run
from emuc import EmuSrvClient, LLCMClient

serv_url = 'http://127.0.0.1:4999'
emu_url = 'http://127.0.0.1:5000'


def measure_ns1():
    """"Measure the time for packaging, onboarding, and instantiating NS1"""

    # start vim-emu, sleep for 10s to wait until it's ready
    print("Starting vim-emu")
    response = requests.post(serv_url).text
    sleep(10)

    # packaging
    print("Packaging")
    start = timer()
    run(['tng-pkg', '-p', '../sdk-projects/tng-smpilot-ns1-emulator'])
    packaging_done = timer()
    packaging_time = packaging_done - start
    print("Packaging time: {}s".format(packaging_time))

    # on-boarding
    # TODO: path
    files = {'package': open('eu.5gtango.tng-smpilot-ns1-emulator.0.1.tgo', 'rb')}
    response = requests.post(emu_url + 'packages', files=files)
    print(response.text)

    # stop emulator
    requests.delete(serv_url)


if __name__ == '__main__':
    # measure_ns1()


    srv_client = EmuSrvClient(serv_url)
    llcm_client = LLCMClient(emu_url)

    # start emulation
    print("Starting vim-emu")
    srv_client.start_emulation()

    # wait for it to be ready
    print("Waiting for it to be ready")
    srv_client.wait_emulation_ready(llcm_client)
    print("ready")
