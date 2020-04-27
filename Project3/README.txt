
README file
-----------
Name: Idan Levi             NetId: il177
Name: Luis Figueroa-Gil     NetId: lef72

1. The ip addr command was used to set up the interface for each node where the address and device were previously given. i.e:
    h1 ip addr add 10.0.0.2 dev h1-eth0

The ip route command was used to set up the default route for each end point through its device. i.e:
    h1 ip route add default via 10.0.0.2

The ip route command was used to set up the per-destination routes for each destination end point through its port. i.e:
    r1 ip route add 10.0.0.2 via 10.0.0.1

2. Are there known issues or functions that aren't working currently in your attached code? If so, explain.

There are not any known issues in the attached code.

3. What problems did you face developing code for this project?

Setting up the default route for each point was somewhat tricky due to the lack of knowledge of the proper use of the ip route command. But, after reading proper documentation and some trial and error it became easier to set up the default routes.

4. What did you learn by working on this project?

First of all, we learned how to set up a virtual machine and run basic commands on mininet's python API.
Moreover, we learned that there are different network topologies and that you can create your own according to its functionality.
In addition, we learned that the mininet shell, hosts, router, and the VM share the same file for creating network topologies; which for this specific project, we used an IP router and four end points.
