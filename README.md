Deployment Script of MPI Cluster
====================================

This script build MPI Cluster on OpenStack instances.

Requirements
---------------
* Python 2.7
* Fabric
* Instances with Ephemeral storage(/dev/vdb).

How to
--------
This example is to build 1 nfs node and 3 compute nodes with image id 6d2bca76-8fff-4d57-9f29-50378539b4fa.

Boot 1 nfs nodes, 3 compute nodes.
```
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name key1 ktanaka-mgmt
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name key1 ktanaka-cmpt01
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name key1 ktanaka-cmpt02
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name key1 ktanaka-cmpt03

nova list|grep ktanaka
| 2c90dbdc-f4bf-4bdd-a91f-c68e6a943dc1 | ktanaka-mgmt    | ACTIVE  | vlan102=10.1.2.107, 172.20.101.112 |
| 17a420e5-f6fd-4f00-805e-dfca36b89e71 | ktanaka-cmpt01   | ACTIVE  | vlan102=10.1.2.114, 172.20.101.109 |
| dc7ca416-0db9-40b4-a74e-8e7e532b0c51 | ktanaka-cmpt02   | ACTIVE  | vlan102=10.1.2.103, 172.20.101.113 |
| 26914719-a173-4254-8d18-05c220ef2720 | ktanaka-cmpt03   | ACTIVE  | vlan102=10.1.2.136, 172.20.101.143 |
```

Download the script.
```
git clone https://github.com/kjtanaka/deploy_mpicluster.git
cd deploy_mpicluster
```

Install management node
```
fab -H 172.20.101.112 setup_mgmt:subnet=10.1.2.0/24
```

Install compute nodes
```
fab -H 172.20.101.109,172.20.101.113,172.20.101.143 setup_compute:mgmt=ktanaka-mgmt
```

The installation is done and you should be able to run mpi on ktanaka-cmpt01, ktanaka-cmpt02 and ktanaka-cmpt03.

I tested Intel MPI Benchmarks 3.2.3 and it runs fine.
