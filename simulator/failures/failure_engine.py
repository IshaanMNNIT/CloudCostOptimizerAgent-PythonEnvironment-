import random

class FailureEngine:
    def __init__(self, failure_probability=0.01, recovery_delay=5):
        self.failure_probability = failure_probability
        self.recovery_delay = recovery_delay
        
        # Tracking which types failed (Critical for Heterogeneous pools)
        self.failed_pool = [] 

    def trigger_failures(self, active_vms_dict):
        """
        Theory: Probabilistic Failure based on fleet size.
        """
        total_failed_this_step = {}
        
        for vm_type, count in active_vms_dict.items():
            if count <= 0: continue
            
            # Realism: Larger fleets have a higher chance of seeing at least one failure
            # P(at least one failure) = 1 - (1 - p)^count
            actual_prob = 1 - (1 - self.failure_probability)**count
            
            if random.random() < actual_prob:
                self.failed_pool.append({
                    "type": vm_type,
                    "remaining_recovery": self.recovery_delay
                })
                total_failed_this_step[vm_type] = total_failed_this_step.get(vm_type, 0) + 1
        
        return total_failed_this_step

    def step(self):
        """
        Theory: Models the 'Self-Healing' nature of modern cloud planes.
        """
        recovered_vms = {}
        still_failing = []

        for vm in self.failed_pool:
            vm["remaining_recovery"] -= 1
            if vm["remaining_recovery"] <= 0:
                v_type = vm["type"]
                recovered_vms[v_type] = recovered_vms.get(v_type, 0) + 1
            else:
                still_failing.append(vm)

        self.failed_pool = still_failing
        return recovered_vms

    def get_state(self):
        return {
            "total_failed_vms": len(self.failed_pool),
            "is_system_degraded": len(self.failed_pool) > 0
        }