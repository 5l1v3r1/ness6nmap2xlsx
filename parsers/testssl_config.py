#!/usr/bin/env python3
#    Copyright (C) 2017 - 2019 Alexandre Teyar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
#    limitations under the License.

# add/remove entries from the dictionaries below to enable/disable
# the reporting of the selected entries - case-sensitive
certificates = {
    "cert_chain_of_trust": {
        "name": "Chain of Trust"
    },
    "cert_expiration_status": {
        "name": "Expired"
    },
    "cert_signatureAlgorithm": {
        "name": "Weak Hashing Algorithm"
    },
    "cert_trust": {
        "name": "Trust"
    }
}

protocols = [
    "SSLv2",
    "SSLv3",
    "TLS1",
    "TLS1_1",
    "TLS1_2",
    "TLS1_3"
]

vulnerabilities = {
    "BEAST": {
        "name": "BEAST"
    },
    "BREACH": {
        "name": "BREACH"
    },
    "CRIME_TLS": {
        "name": "CRIME"
    },
    # "fallback_SCSV": {
    #     "name": "Fallback SCSV"
    # },
    "FREAK": {
        "name": "FREAK"
    },
    "LOGJAM-common_primes": {
        "name": "Logjam Common Primes"
    },
    "LOGJAM": {
        "name": "Logjam"
    },
    "LUCKY13": {
        "name": "Lucky13"
    },
    "POODLE_SSL": {
        "name": "POODLE"
    },
    "RC4": {
        "name": "RC4"
    },
    "ROBOT": {
        "name": "ROBOT"
    },
    "secure_client_renego": {
        "name": "Secure Client Renegotiation"
    },
    "SWEET32": {
        "name": "Sweet32"
    }
}
