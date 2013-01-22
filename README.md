Deployment Script of MPI Cluster
====================================

This script build MPI Cluster on Ubuntu-12.04/12.10 instances on OpenStack.

Requirements
---------------
* Python
* Fabric
* Nova Client
* OpenStack
* Instances with Ephemeral storage (on /dev/vdb)

How to
--------
This example is to build 1 nfs node and 3 compute nodes with image id 6d2bca76-8fff-4d57-9f29-50378539b4fa.
```
nova image-list|grep common
| 6d2bca76-8fff-4d57-9f29-50378539b4fa | common/precise-server-cloudimg-amd64.img.manifest.xml | ACTIVE | |
```

Boot 4 instances(1 nfs nodes, 3 compute nodes).
```
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name your_key your-mgmt
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name your_key your-cmpt01
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name your_key your-cmpt02
nova boot --image 6d2bca76-8fff-4d57-9f29-50378539b4fa --flavor m1.medium --key-name your_key your-cmpt03

nova list|grep your-
| 2c90dbdc-f4bf-4bdd-a91f-c68e6a943dc1 | your-mgmt     | ACTIVE  | vlan102=10.1.2.107, 172.20.101.112 |
| 17a420e5-f6fd-4f00-805e-dfca36b89e71 | your-cmpt01   | ACTIVE  | vlan102=10.1.2.114, 172.20.101.109 |
| dc7ca416-0db9-40b4-a74e-8e7e532b0c51 | your-cmpt02   | ACTIVE  | vlan102=10.1.2.103, 172.20.101.113 |
| 26914719-a173-4254-8d18-05c220ef2720 | your-cmpt03   | ACTIVE  | vlan102=10.1.2.136, 172.20.101.143 |
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
fab -H 172.20.101.109,172.20.101.113,172.20.101.143 setup_compute:mgmt=your-mgmt
```

The installation is done and you should be able to login as ubuntu, and able to run MPI on your compute nodes.

```
ssh ubuntu@172.20.101.109
mpicc ....
mpirun -np 6 -host your-cmpt01,your-cmpt02,your-cmpt03 ...
```
By the way, shared scratch space is /scratch. Check your /etc/fstab for more information.

Want to try Intel MPI Benchmarks 3.2.3?
----------------------------------
If you want to try some benchmark, Intel MPI Benchmarks 3.2.3 is good and easy to try.
Download it from the link.

http://software.intel.com/en-us/articles/intel-mpi-benchmarks/

And run this command with one of your compute node.
```
fab -H 172.20.101.109 install_IMB_3_2_3:tarfile=/path/to/your/IMB_3.2.3.tgz
```

Now you can run the benchmark. So login to one of your compute nodes and try benchmark.
```
ssh ubuntu@172.20.101.109
mpirun -np 2 -host your-cmpt01,your-cmpt02 imb_3.2.3/src/IMB-MPI1 pingpong
mpirun -np 6 -host your-cmpt01,your-cmpt02,your-cmpt03 imb_3.2.3/src/IMB-MPI1 bcast
```

For more information, read imb_3.2.3/doc/ReadMe_IMB.txt.
