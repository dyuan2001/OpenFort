#include <stdio.h>
#include <stdlib.h>
#include <mach/mach_init.h>
#include <sys/sysctl.h>
#include <mach/mach_vm.h>
#include <libproc.h>

int findpid(char *name) {
    pid_t pids[2048];
    int bytes = proc_listpids(PROC_ALL_PIDS, 0, pids, sizeof(pids));
    int n_proc = bytes / sizeof(pids[0]);
    pid_t proc_match = 0;
    for (int i = 0; i < n_proc; i++) {
        struct proc_bsdinfo proc;
        int st = proc_pidinfo(pids[i], PROC_PIDTBSDINFO, 0, &proc, PROC_PIDTBSDINFO_SIZE);
        if (st == PROC_PIDTBSDINFO_SIZE && strcmp(name, proc.pbi_name) == 0) {
            printf("%d [%d] [%s] [%s]\n", pids[i], proc.pbi_ppid, proc.pbi_comm, proc.pbi_name);
            proc_match = pids[i];
            break;
        }
    }
    if (proc_match == 0) return -1;
    else return proc_match;
}

/**
 * @brief Find base address of a given pid.
 * Taken from https://stackoverflow.com/questions/10301542/getting-process-base-address-in-mac-osx.
 * 
 * @param pid Process id.
 * @param baseAddr Buffer where base address should be stored.
 * @return int 0 on success, 1 on failure.
 */
int findBaseAddr(pid_t pid, mach_port_name_t task, uint64_t *baseAddr) {
    // TODO: Change task to use user-defined name and return baseaddr instead of int
    vm_map_offset_t vmoffset;
    vm_map_size_t vmsize;
    uint32_t nesting_depth = 0;
    struct vm_region_submap_info_64 vbr;
    mach_msg_type_number_t vbrcount = 16;
    kern_return_t kr;

    if ((kr = mach_vm_region_recurse(task, &vmoffset, &vmsize,
                 &nesting_depth,
                 (vm_region_recurse_info_t)&vbr,
                 &vbrcount)) != KERN_SUCCESS) return 1;
    else {
        *baseAddr = vmoffset;
        return 0;
    }
}

int readProcessMemory(int pid, uint64_t address, char *buf, uint64_t size) {
    return 0;
}

int main() {
    char name[20];
    pid_t pid;
    mach_port_t task;
    kern_return_t kret;
    uint64_t baseAddr;
    

    printf("Enter name of program to find pid for: ");
    scanf("%s", name);

    if ((pid = findpid(name)) == -1) {
        printf("findpid failed\n");
        goto bad;
    }
    if ((kret = task_for_pid(mach_task_self(), pid, &task)) != KERN_SUCCESS) {
        printf("taskforpid failed, %d\n", kret);
        goto bad;
    }
    if (findBaseAddr(pid, task, &baseAddr) == 1) {
        printf("findBaseAddr failed\n");
        goto bad;
    }
    

    printf("done, baseAddr = %llx\n", baseAddr);
    return 0;

    bad:
        printf("something went wrong");
        return 1;
}