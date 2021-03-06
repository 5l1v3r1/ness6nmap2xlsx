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

# TODO:
# * fix error when no table_data is passed to draw_table
# * decide whether to keep the file column or not

from .parser import Parser
from .testssl_config import *

import json
import logging
import xlsxwriter


class Testssl(Parser):
    def __init__(self, input_files, output_file):
        super(Testssl, self).__init__(input_files, output_file)

    def print_vars(self):
        logging.info("input file(s): {}".format(
            sorted([x.name for x in self._input_files])))
        logging.info("output file: {}".format(self._output_file))
        logging.info("certificate issue(s) to process: {}".format(
            sorted(certificates.keys())))
        logging.info("protocol(s) to process: {}".format(
            sorted(protocols)))
        logging.info("vulnerability/ies to process: {}".format(
            sorted(vulnerabilities.keys())))

    def parse(self):
        logging.info("generating worksheet 'Host vs Certificate'...")
        self.parse_host_certificate()
        logging.info("generating worksheet 'Host vs Certificates'...")
        self.parse_host_certificates()
        logging.info("generating worksheet 'Host vs Protocol'...")
        self.parse_host_protocol()
        logging.info("generating worksheet 'Host vs Protocols'...")
        self.parse_host_protocols()
        logging.info("generating worksheet 'Host vs Vulnerability'...")
        self.parse_host_vulnerability()
        logging.info("generating worksheet 'Host vs Vulnerabilities'...")
        self.parse_host_vulnerabilities()

        try:
            self._workbook.close()
        except Exception as e:
            logging.exception("{}".format(e))

    def parse_host_certificate(self):
        table_data = []
        table_headers = [
            {"header": "Host IP"},
            {"header": "Port"},
            {"header": "Vulnerability"},
            {"header": "Severity"},
            {"header": "Information"}
        ]

        try:
            for input_file in self._input_files:
                input_file.seek(0)
                data = json.load(input_file)

                for values in data["scanResult"]:
                    for serverDefault in values["serverDefaults"]:
                        if serverDefault["id"] in certificates.keys():
                            table_data.append(
                                [
                                    values["ip"],
                                    int(values["port"]),
                                    certificates[serverDefault["id"]]["name"],
                                    serverDefault["severity"],
                                    serverDefault["finding"]
                                ]
                            )

            worksheet = self._workbook.add_worksheet("Host vs Certificate")
            self.draw_table(worksheet, table_headers, table_data)
        except KeyError as e:
            logging.exception("KeyError: {}".format(e))
        except ValueError as e:
            logging.exception("ValueError: {}".format(e))

    def parse_host_certificates(self):
        table_data = []
        table_headers = [
            {"header": "Host IP"},
            {"header": "Port"}
        ]

        for values in certificates.values():
            table_headers.append({"header": values["name"]})

        try:
            for input_file in self._input_files:
                input_file.seek(0)
                data = json.load(input_file)

                for values in data["scanResult"]:
                    d = {
                        "Host IP": values["ip"],
                        "Port": int(values["port"])
                    }

                    for serverDefault in values["serverDefaults"]:
                        if serverDefault["id"] in certificates.keys():
                            d[serverDefault["id"]] = {
                                "name": certificates[serverDefault["id"]]["name"],
                                "severity": serverDefault["severity"]
                            }

                    table_data.append(
                        insert_at_index([x["header"] for x in table_headers], d))

            worksheet = self._workbook.add_worksheet("Host vs Certificates")
            self.draw_table(worksheet, table_headers, table_data)
        except KeyError as e:
            logging.exception("KeyError: {}".format(e))
        except ValueError as e:
            logging.exception("ValueError: {}".format(e))

    def parse_host_protocol(self):
        table_data = []
        table_headers = [
            {"header": "Host IP"},
            {"header": "Port"},
            {"header": "Supported Protocol"},
            {"header": "Severity"}
        ]

        try:
            for input_file in self._input_files:
                input_file.seek(0)
                data = json.load(input_file)

                for values in data["scanResult"]:
                    for protocol in values["protocols"]:
                        if protocol["id"] in protocols:
                            if protocol["finding"] == "offered":
                                table_data.append(
                                    [
                                        values["ip"],
                                        int(values["port"]),
                                        protocol["id"],
                                        protocol["severity"]
                                    ]
                                )

            worksheet = self._workbook.add_worksheet("Host vs Protocol")
            self.draw_table(worksheet, table_headers, table_data)
        except KeyError as e:
            logging.exception("KeyError: {}".format(e))
        except ValueError as e:
            logging.exception("ValueError: {}".format(e))

    def parse_host_protocols(self):
        table_data = []
        table_headers = [
            {"header": "Host IP"},
            {"header": "Port"}
        ]

        for protocol in protocols:
            table_headers.append({"header": protocol})

        try:
            for input_file in self._input_files:
                input_file.seek(0)
                data = json.load(input_file)

                for values in data["scanResult"]:
                    d = {
                        "Host IP": values["ip"],
                        "Port": int(values["port"])
                    }

                    for protocol in values["protocols"]:
                        if protocol["id"] in protocols:
                            if protocol["finding"] == "offered":
                                d[protocol["id"]] = "YES"
                            else:
                                d[protocol["id"]] = "NO"

                    table_data.append(
                        insert_at_index([x["header"] for x in table_headers], d))

            worksheet = self._workbook.add_worksheet("Host vs Protocols")
            self.draw_table(worksheet, table_headers, table_data)
        except KeyError as e:
            logging.exception("KeyError: {}".format(e))
        except ValueError as e:
            logging.exception("ValueError: {}".format(e))

    def parse_host_vulnerability(self):
        table_data = []
        table_headers = [
            {"header": "Host IP"},
            {"header": "Port"},
            {"header": "Vulnerability"},
            {"header": "Severity"},
            {"header": "CVE"},
            {"header": "Information"}
        ]

        try:
            for input_file in self._input_files:
                input_file.seek(0)
                data = json.load(input_file)

                for values in data["scanResult"]:
                    for vulnerability in values["vulnerabilities"]:
                        if vulnerability["id"] in vulnerabilities.keys():
                            table_data.append(
                                [
                                    values["ip"],
                                    int(values["port"]),
                                    vulnerabilities[vulnerability["id"]]["name"],
                                    vulnerability["severity"],
                                    # avoid to raise KeyError exceptions for the
                                    # entries without CVE number and replace space
                                    # with a comma
                                    vulnerability.get("cve", "N/A")
                                    .replace(" ", ", "),
                                    vulnerability["finding"]
                                ]
                            )

            worksheet = self._workbook.add_worksheet("Host vs Vulnerability")
            self.draw_table(worksheet, table_headers, table_data)
        except KeyError as e:
            logging.exception("KeyError: {}".format(e))
        except ValueError as e:
            logging.exception("ValueError: {}".format(e))

    def parse_host_vulnerabilities(self):
        table_data = []
        table_headers = [
            {"header": "Host IP"},
            {"header": "Port"}
        ]

        for values in vulnerabilities.values():
            table_headers.append({"header": values["name"]})

        try:
            for input_file in self._input_files:
                input_file.seek(0)
                data = json.load(input_file)

                for values in data["scanResult"]:
                    d = {
                        "Host IP": values["ip"],
                        "Port": int(values["port"])
                    }

                    for vulnerability in values["vulnerabilities"]:
                        if vulnerability["id"] in vulnerabilities.keys():
                            d[vulnerability["id"]] = {
                                "name": vulnerabilities[vulnerability["id"]]
                                ["name"],
                                "severity": vulnerability["severity"]
                            }

                    table_data.append(
                        insert_at_index([x["header"] for x in table_headers], d))

            worksheet = self._workbook.add_worksheet("Host vs Vulnerabilities")
            self.draw_table(worksheet, table_headers, table_data)
        except KeyError as e:
            logging.exception("KeyError: {}".format(e))
        except ValueError as e:
            logging.exception("ValueError: {}".format(e))


def insert_at_index(headers, d):
    """ insert values at the appropriate index
    """
    data = ["N/A"] * len(headers)

    for key, values in d.items():
        if isinstance(values, dict):
            data[headers.index(values["name"])] = values.get("severity")
        else:
            data[headers.index(key)] = values

    return data
