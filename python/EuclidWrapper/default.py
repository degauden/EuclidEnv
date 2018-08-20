from __future__ import division, print_function

import argparse
import os
from lxml import etree

from EuclidWrapper.logging import logger


def defineWrapperProgramOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ecdm_config_xml', type=str, help='The XML config file')
    parser.add_argument('--ecdm_config_xpath', type=str,
                        default="//ConfigurationFile[ModuleName='{}']/FileContainer/FileName",
                        help='The XPath to be used for extracting the Elements config file')
    parser.add_argument('--forward_ecdm_config_xml', type=str,
                        help='The parameter name to forward the ecdm_config_xml to')
    return parser


def getOptionsToAppend(args, executable):
    options = []

    if args.ecdm_config_xml:
        xpath = args.ecdm_config_xpath.replace('{}', executable)
        logger.info('Parsing XML configuration file: {}'.format(args.ecdm_config_xml))
        tree = etree.parse(args.ecdm_config_xml)
        logger.info('Locating Elements config file with XPath: {}'.format(xpath))
        conf_list = tree.xpath(xpath)
        if len(conf_list) == 0:
            logger.error('Failed to find the config file element using XPath')
            exit(1)
        if len(conf_list) > 1:
            logger.error('XPath query matched multiple config files')
            exit(1)
        conf_file = os.path.join('data', conf_list[0].text.strip())
        logger.info('Found Elements config file: {}'.format(conf_file))
        options.append('--config-file')
        options.append(conf_file)

        if args.forward_ecdm_config_xml:
            options.append('--' + args.forward_ecdm_config_xml)
            options.append(args.ecdm_config_xml)

    return options

