# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
 
  config.ssh.insert_key = false

  ansible_groups= {
   "openbsd_dns"  => [
        "dns1",
   ],
   "home_clients" => [
        "clientdns1",
   ],
  } 

 
  config.vm.define "dns1", autostart: true do |dns1|
    dns1.vm.synced_folder ".", "/vagrant", disabled: true
    dns1.vm.hostname ="dns1"
    dns1.vm.box="trombik/ansible-openbsd-6.0-amd64"
    dns1.vm.box_check_update = false
    dns1.vm.network "private_network", ip: "172.31.1.254", netmask: "255.255.255.0",
      virtualbox__intnet: "home"
    dns1.vm.provider "virtualbox" do |vb|
      vb.gui = false
      vb.memory = "256"
      vb.name = "dns1"
    end
    dns1.vm.provision "shell",run: "always", inline: <<-SHELL
#      (route -n show | grep default | grep em1 )  || ( ( route delete default || true ) && route add -inet 0/0 172.31.3.251 )
#      (grep 'interface \\"em0\\" ' /etc/dhclient.conf || sh -c "echo 'interface \\"em0\\" { ignore routers,domain-name-servers;}' >> /etc/dhclient.conf" )
      ln -sf /usr/local/bin/python /usr/bin/python
    SHELL
    dns1.vm.provision "ansible" do |ansible|
      ansible.groups = ansible_groups
      ansible.playbook = "provisioning/playbook.yml"
    end

  end

  config.vm.define "dnsclient1", autostart: true do |dnsclient1|
    dnsclient1.vm.synced_folder ".", "/vagrant", disabled: true
    dnsclient1.vm.hostname ="dnsclient1"
    dnsclient1.vm.box="trombik/ansible-openbsd-6.0-amd64"
    dnsclient1.vm.box_check_update = false
    dnsclient1.vm.network "private_network", ip: "172.31.1.10", netmask: "255.255.255.0",
      virtualbox__intnet: "home"

    dnsclient1.vm.provider "virtualbox" do |vb|
      vb.gui = false
      vb.memory = "256"
      vb.name = "dnsclient1"
    end
    dnsclient1.vm.provision "shell", run: "always",inline: <<-SHELL
#      (route -n show | grep default | grep em1 )  || ( (route delete default || true ) && route add -inet 0/0 172.31.1.254 )
#      (grep 'interface \\"em0\\" ' /etc/dhclient.conf || sh -c "echo 'interface \\"em0\\" { ignore routers,domain-name-servers;}' >> /etc/dhclient.conf" )
      ln -sf /usr/local/bin/python /usr/bin/python
    SHELL
    dnsclient1.vm.provision "ansible" do |ansible|
      ansible.groups = ansible_groups
      ansible.playbook = "provisioning/playbook.yml"
    end

  end


#end final
end

