#!/usr/bin/env python

import os.path
from fabric.api import run, sudo, settings, abort, put, cd, env
from fabric.contrib.console import confirm
from fabric.decorators import runs_once

env.user = 'ubuntu'
#env.parallel=True

def setup_mgmt(subnet):
  sudo ('apt-get update', pty=True)
  sudo('apt-get -y install nfs-server build-essential', pty=True)

  with cd('~/'):
    run('ssh-keygen -N "" -f .ssh/id_rsa')
    run('cat .ssh/id_rsa.pub >> .ssh/authorized_keys')
    run('echo "StrictHostKeyChecking no" >> .ssh/config')
    run('echo "UserKnownHostsFile=/dev/null" >> .ssh/config')

  sudo('mkdir /scratch', pty=True)
  sudo('mount /dev/vdb /scratch', pty=True)
  sudo('mkdir /scratch/ubuntu', pty=True)
  sudo('chown -R ubuntu:ubuntu /scratch/ubuntu', pty=True)
  sudo('echo "/scratch %s(rw,sync,no_subtree_check)" >> /etc/exports' % (subnet), pty=True)
  sudo('echo "/home %s(rw,sync,no_subtree_check)" >> /etc/exports' % (subnet), pty=True)
  sudo('exportfs -ra', pty=True)

def setup_compute(mgmt):
  sudo ('apt-get update', pty=True)
  sudo('apt-get -y install nfs-client openmpi-bin mpi-default-dev build-essential', pty=True)
  sudo('ln -s /usr/bin/make /usr/bin/gmake', pty=True)
  sudo('mkdir /scratch', pty=True)
  sudo("echo %s:/scratch /scratch nfs rsize=8192,wsize=8192,timeo=14,intr >> /etc/fstab" % (mgmt),
       pty=True)
  sudo("echo %s:/home /home nfs rsize=8192,wsize=8192,timeo=14,intr >> /etc/fstab" % (mgmt), pty=True)
  sudo('mount -a', pty=True)

def install_IMB_3_2_3(tarfile):
  put("%s" % tarfile, "~/IMB_3.2.3.tgz")
  with cd('~/'):
    run('tar zxvf IMB_3.2.3.tgz')
  with cd('~/imb_3.2.3/src'):
    run('make')
