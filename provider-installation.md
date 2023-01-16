# Provider installation 
- Make sure you have enabled IOMMU in BIOS
- Install Golem as provider: https://handbook.golem.network/provider-tutorials/provider-tutorial
- git clone https://github.com/norbibi/golem_cuda and run `./configure.sh`. Follow the installer.
- Reboot system
- You can optionally test if your GPU is properly visible in VM by:
  * install ya-runtime-dbg: https://github.com/golemfactory/ya-runtime-dbg/releases
  * download testing image: http://gpu-on-golem.s3.eu-central-1.amazonaws.com/golem_cuda_base-d9981476ceecb823bfc3b076f93c65eea608e19dce306b6dc1f6a0ff.gvmi
  * set GPU_PCI environmental variable `export GPU_PCI=[value]`. You can check the `value` in the `/etc/systemd/system/golem_provider.service` file.
  * run debug runtime with: `ya-runtime-dbg --runtime /home/$USER/.local/lib/yagna/plugins/ya-runtime-vm/ya-runtime-vm --task-package golem_cuda_base-d9981476ceecb823bfc3b076f93c65eea608e19dce306b6dc1f6a0ff.gvmi --workdir /tmp/workdir`
  * while in the runtime run `lspci -vnn` and look for your device or run nvidia-smi and check if you device is visible
- Adjust service file `sudo nano /etc/systemd/system/golem_provider.service`:
  * set subnet
  * set payment network
- enable service:
  * `sudo systemctl enable --now golem_provider.service`
- check the logs
  * `journalctl -e -u golem_provider.service`

In case of problems look below for tips.

### max locked memory limit
There might be a problem with the limit on locked memory while running VM from the command line or as a service. Ex. error message in dmesg: vfio_pin_pages_remote: RLIMIT_MEMLOCK (67108864) exceeded It relates to max locked memory limit which can be checked with ulimit -Ha. golem_provider.service defines LimitMEMLOCK=infinity which should work. But if it's not working, one can try to overcome this by adding golem - memlock unlimited to /etc/security/limits.conf file.

### GPU being used in host system
There might be a problem when running VM 
`vfio-pci 0000:4a:00.0: BAR 0: can’t reserve [mem 0xc0000000-0xcffffffff 64bit pref]`
It means that GPU is probably used by the host machine.
One can try to use:
* [tip #1](https://wiki.installgentoo.com/index.php/PCI_passthrough#Step_3:_Block_access_on_your_physical_OS_to_the_GPU) 
* [tip #2](https://forum.proxmox.com/threads/gpu-passthrough-issues-after-upgrade-to-7-2.109051/#post-469855)
* or add `video=efifb:off` option to kernel command line (`/etc/default/grub`)


## GPU_PCI environment variable
While trying to run ya-runtime-vm (using ya-runtime-dbg) from the command line one must have the GPU_PCI variable set. Otherwise, no GPU will be mapped into VM.
In _golem_provider.service_ the variable is configured properly.
