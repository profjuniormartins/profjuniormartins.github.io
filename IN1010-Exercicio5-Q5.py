#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, s3, bw=100, delay='1ms', max_queue_size=100, loss=1)
    net.addLink(s1, s2, bw=100, delay='1ms', max_queue_size=100, loss=1)
    net.addLink(s3, s4, bw=100, delay='1ms', max_queue_size=100, loss=1)
    net.addLink(s4, s2, bw=100, delay='1ms', max_queue_size=100, loss=1)
    net.addLink(s2, s5, bw=100, delay='1ms', max_queue_size=100, loss=1)
    net.addLink(h3, s3, bw=100, loss=0.5)
    net.addLink(h4, s4, bw=100, loss=0.5)
    net.addLink(s4, h5, bw=100, loss=0.5)
    net.addLink(h2, s1, bw=100, loss=0.5)
    net.addLink(h1, s1, bw=100, loss=0.5)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([])
    net.get('s1').start([])
    net.get('s4').start([])
    net.get('s3').start([])
    net.get('s5').start([])

    info( '*** Post configure switches and hosts\n')
    net.addLink(h2, s1, bw=100, delay='1ms')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
