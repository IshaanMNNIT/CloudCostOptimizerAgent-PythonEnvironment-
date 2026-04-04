class VMManager:
    # High-Fidelity Resource Catalog
    # Theory: Defines the Action-Space Mapping and Cost-Benefit Trade-offs
    VM_TYPES = {
        "small": {
            "capacity": 100,
            "cost": 2,
            "startup_delay": 2
        },
        "medium": {
            "capacity": 250,
            "cost": 5,
            "startup_delay": 3
        },
        "large": {
            "capacity": 500,
            "cost": 10,
            "startup_delay": 5
        }
    }

    def __init__(self, cooldown_period=5):
        # Initial State: Start with a 'Heartbeat' capacity
        self.active_vms = {
            "small": 2,
            "medium": 0,
            "large": 0
        }

        self.pending_vms = []
        self.cooldown_remaining = 0
        self.cooldown_period = cooldown_period

    def step(self):
        """
        Progresses the internal clock of the compute pool.
        Theory: Implements the 'Transition Dynamics' of the environment.
        """
        self._update_pending_vms()
        self._update_cooldown()

    def scale_up(self, vm_type="small", count=1):
        """
        Logic: Resource Provisioning with Boot Delay.
        Theory: Introduces 'Lag' between Action and Reward.
        """
        if self.cooldown_remaining > 0:
            return False

        if vm_type not in self.VM_TYPES:
            return False

        delay = self.VM_TYPES[vm_type]["startup_delay"]

        for _ in range(count):
            self.pending_vms.append({
                "type": vm_type,
                "remaining_delay": delay
            })

        # Set Cooldown: Prevents 'Policy Thrashing'
        self.cooldown_remaining = self.cooldown_period
        return True

    def scale_down(self, vm_type="small", count=1):
        """
        Logic: Graceful De-provisioning with Safety Guard.
        Theory: Prevents 'Zero-State' failure where system cannot recover.
        """
        if self.cooldown_remaining > 0:
            return False

        current_count = self.active_vms[vm_type]
        
        # Safety Guard: Ensure at least 1 small VM always exists (The Heartbeat)
        if vm_type == "small":
            actual_to_remove = min(count, current_count - 1)
        else:
            actual_to_remove = min(count, current_count)

        self.active_vms[vm_type] -= max(0, actual_to_remove)
        
        self.cooldown_remaining = self.cooldown_period
        return True

    def _update_pending_vms(self):
        """
        Internal Timer: Moves VMs from 'Pending' to 'Active'.
        """
        updated_pending = []

        for vm in self.pending_vms:
            vm["remaining_delay"] -= 1

            if vm["remaining_delay"] <= 0:
                self.active_vms[vm["type"]] += 1
            else:
                updated_pending.append(vm)

        self.pending_vms = updated_pending

    def _update_cooldown(self):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1

    def get_total_capacity(self):
        return sum(count * self.VM_TYPES[vt]["capacity"] for vt, count in self.active_vms.items())

    def get_pending_capacity(self):
        """
        New Metric: In-Flight Capacity.
        Theory: Solves 'State Aliasing'—helps agent know if help is coming.
        """
        return sum(self.VM_TYPES[vm["type"]]["capacity"] for vm in self.pending_vms)

    def get_total_cost(self):
        return sum(count * self.VM_TYPES[vt]["cost"] for vt, count in self.active_vms.items())

    def get_state(self):
        """
        Theory: Returns the Compute component of the Observation Vector O_t.
        """
        return {
            "small_vms": self.active_vms["small"],
            "medium_vms": self.active_vms["medium"],
            "large_vms": self.active_vms["large"],
            "pending_count": len(self.pending_vms),
            "pending_capacity": self.get_pending_capacity(),
            "cooldown_remaining": self.cooldown_remaining,
            "total_active_capacity": self.get_total_capacity(),
            "total_hourly_cost": self.get_total_cost()
        }