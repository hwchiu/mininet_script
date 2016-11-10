#!/usr/bin/env python

from mininet.cli import CLI
from mininet.node import Link
from mininet.net import Mininet
from mininet.node import Controller
from mininet.term import makeTerm
#from functools import partial
from sets import Set

def SortToplogy(data):
    (sDevTmp, sInfTmp, dDevTmp, dInfTmp) = line.split()
    if sDevTmp > dDevTmp:
        return (sDevTmp, sInfTmp, dDevTmp, dInfTmp)
    else:
        return (dDevTmp, dInfTmp, sDevTmp, sInfTmp)


def CollectTopology(topology, sDev, dDev, links):
    if not sDev in topology:
        topology[sDev] = {}
    if not dDev in topology[sDev]:
        topology[sDev][dDev] = {}
    topology[sDev][dDev] = links

def CreateSwitch(net, sDev, switchs):
    if not sDev in switchs:
        switchs[sDev] = net.addSwitch(sDev)

def CreateLink(net, sDev, dDev, sInf, dInf):
    print sDev, dDev, sInf, dInf
    net.addLink(sDev, dDev, intfName1=sInf, intfName2=dInf)

if '__main__' == __name__:
	
    net = Mininet()
    topology = {}
    switchs = {}
    with open('topology.txt', 'r') as f:
        for line in f.readlines():
            (sDev, sInf, dDev, dInf) = SortToplogy(line)
            CollectTopology(topology, sDev, dDev, (sInf, dInf))
    for sDev in topology:
        CreateSwitch(net, sDev, switchs)
        for dDev in topology[sDev]:
            links = topology[sDev][dDev]
            CreateSwitch(net, dDev, switchs)
            CreateLink(net, switchs[sDev], switchs[dDev], sDev + "-" + links[0], dDev + "-" + links[1])

    c0 = Controller('c0')
    net.build()
    c0.start()

    for s in switchs:
        switchs[s].start([c0])

    CLI(net)
    net.stop()
