
# Docker 101

This is an introductory course to containerization
and [Docker](https://docker.com).

The course will cover:

1. computational resources and the Operating System's Kernel
1. Virtualization: pros and cons
1. Processes & isolation tools
1. Containers & Docker
1. Containerization as an application packaging system
1. Practice session

---

## Computational resources

Computational resources are basically:

- RAM
- Storage
- Network
- CPU

---

## Meet the Kernel

The (Linux) kernel decides *who* and *when*
can access to RAM, CPU and disks using abstractions.

| Physical | Abstraction |
| --- | --- |
| RAM | Virtual Memory |
| CPU | Computational Shares |
| Storage & Network | File descriptors |

```mermaid
graph LR


subgraph apps[ ]
direction LR
browser[Browser fab:fa-firefox-browser]
game[Games fa:fa-chess-knight fa:fa-chess-rook]
word[Editor fa:fa-file-word]
end

subgraph k [ ]
kernel[K\ne\nr\nn\ne\nl\n \nfab:fa-linux]
end

subgraph hw[ ]
direction LR
cpu[CPU fa:fa-cpu]
ram[RAM fa:fa-memory]
storage[HD fa:fa-hdd]
%% net[Net fa:fa-ethernet]
end

apps ~~~ kernel ~~~ hw
```

---

## A process is a cage

The Kernel cages programs.

It only shows them a part of the global resources.

Programs think they have a complete operating system
at their disposal.

A software requests access to resources invoking system calls.

[Image from deviantart](https://www.deviantart.com/mirinata/art/Lucky-Luke-and-the-Daltons-524439744)
![Alt text](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4a9529e8-cf9b-4b7b-a70d-ad27fd90ae1c/d8o8kao-2be99487-2c9f-45f3-9cb1-9343e05d2900.jpg/v1/fill/w_1020,h_783,q_70,strp/lucky_luke_and_the_daltons_by_mirinata_d8o8kao-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzRhOTUyOWU4LWNmOWItNGI3Yi1hNzBkLWFkMjdmZDkwYWUxY1wvZDhvOGthby0yYmU5OTQ4Ny0yYzlmLTQ1ZjMtOWNiMS05MzQzZTA1ZDI5MDAuanBnIiwiaGVpZ2h0IjoiPD03ODYiLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS53YXRlcm1hcmsiXSwid21rIjp7InBhdGgiOiJcL3dtXC80YTk1MjllOC1jZjliLTRiN2ItYTcwZC1hZDI3ZmQ5MGFlMWNcL21pcmluYXRhLTQucG5nIiwib3BhY2l0eSI6OTUsInByb3BvcnRpb25zIjowLjQ1LCJncmF2aXR5IjoiY2VudGVyIn19.J8HEQiHvVmvXba88H0knHm5ZD7xlgMeFAG_rmsW9DXE)
---

## The cage is named "process"

The `ps` command lists the "cages" showing the assigned virtual resources.

```bash
#       process id, executable, %cpu, virtual memory size
! ps -o pid,cmd,pcpu,vsize
```

These resources are retrieved from the `/proc/$PID/stat` and other files.

```bash
! ls /proc/[0-9]*/stat
```

---

## To access hardware, you need syscall

An imaginary dialogue between your browser and your Kernel.

```mermaid
graph TB

subgraph hw
direction LR
cpu[CPU fa:fa-cpu]
ram[RAM fa:fa-memory]
storage[HD fa:fa-hdd]

end
subgraph Linux
l1
l2
l3[...]
end

subgraph Firefox
f1
f2
f3
end

f1("Hey Kernel, I want to save a file on disk!")
l1("Can you tell the magic words?")
f2("open(..);\nwrite(..);\nclose(..);")
l2("Correct!\nThree syscalls!\nI'll notify you when I'm done.")
f3("OK, I'm waiting for you!")
