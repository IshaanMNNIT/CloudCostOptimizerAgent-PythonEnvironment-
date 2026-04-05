import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.Pe;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.vms.Vm;
import org.cloudsimplus.vms.VmSimple;
import org.cloudsimplus.brokers.DatacenterBrokerSimple;
import org.cloudsimplus.cloudlets.Cloudlet;
import org.cloudsimplus.cloudlets.CloudletSimple;
import org.cloudsimplus.utilizationmodels.UtilizationModelDynamic;

import java.io.PrintWriter; // Added for file export
import java.io.File;        // Added for file export
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class StressValidationTest {
    public static void main(String[] args) throws Exception {
        CloudSimPlus simulation = new CloudSimPlus();

        // 1. Datacenter setup (Infrastructure)
        List<HostSimple> hostList = new ArrayList<>();
        for (int h = 0; h < 3; h++) {
            List<Pe> peList = new ArrayList<>();
            for (int i = 0; i < 4; i++) {
                peList.add(new PeSimple(1000));
            }
            HostSimple host = new HostSimple(8192, 10000, 1000000, peList);
            hostList.add(host);
        }

        DatacenterSimple datacenter = new DatacenterSimple(simulation, hostList);
        DatacenterBrokerSimple broker = new DatacenterBrokerSimple(simulation);

        // 2. Read PPO action trace from Python
        List<String> lines = Files.readAllLines(Paths.get("actions.txt"));

        int smallVmCount = 2;
        int mediumVmCount = 0;
        int largeVmCount = 0;

        // 3. Replay PPO actions to determine final VM fleet
        for (String line : lines) {
            if(line.trim().isEmpty()) continue;
            int action = Integer.parseInt(line.trim());
            switch (action) {
                case 1: smallVmCount++; break;
                case 2: mediumVmCount++; break;
                case 3: largeVmCount++; break;
                case 4: smallVmCount = Math.max(1, smallVmCount - 1); break;
                case 5: mediumVmCount = Math.max(0, mediumVmCount - 1); break;
                case 6: largeVmCount = Math.max(0, largeVmCount - 1); break;
                default: break; // Action 0 is No-Op
            }
        }

        // 4. Create the Virtual Machines
        List<Vm> vmList = new ArrayList<>();
        addVms(vmList, smallVmCount, 1000, 1, 2048);
        addVms(vmList, mediumVmCount, 1500, 2, 4096);
        addVms(vmList, largeVmCount, 2000, 4, 8192);
        broker.submitVmList(vmList);

        // 5. Stress workload (Cloudlets)
        List<Cloudlet> cloudletList = new ArrayList<>();
        for (int i = 0; i < 50; i++) { // Increased to match 288-step trace density
            long length = (i >= 15 && i <= 25) || (i >= 35 && i <= 40) ? 15000 : 4000;
            Cloudlet cloudlet = new CloudletSimple(length, 2, new UtilizationModelDynamic(0.6));
            cloudlet.setSizes(1024);
            cloudletList.add(cloudlet);
        }
        broker.submitCloudletList(cloudletList);

        // 6. Run Simulation
        simulation.start();

        // 7. Calculate Metrics
        int totalCapacity = (smallVmCount * 100) + (mediumVmCount * 250) + (largeVmCount * 500);
        double avgFinishTime = broker.getCloudletFinishedList().stream()
                                     .mapToDouble(Cloudlet::getFinishTime)
                                     .average().orElse(0);

        // 8. DATA EXPORT FOR PLOT 9
        // We save this to a CSV so Python can read it for the comparison plot
        try (PrintWriter writer = new PrintWriter(new File("cloudsim_results.csv"))) {
            writer.println("metric,value");
            writer.println("total_capacity," + totalCapacity);
            writer.println("avg_finish_time," + avgFinishTime);
            writer.println("finished_jobs," + broker.getCloudletFinishedList().size());
        }

        // Print to console for immediate feedback
        System.out.println("========================================");
        System.out.println("VALIDATION EXPORT COMPLETE");
        System.out.println("Avg Finish Time: " + avgFinishTime);
        System.out.println("========================================");
    }

    private static void addVms(List<Vm> list, int count, int mips, int pes, int ram) {
        for (int i = 0; i < count; i++) {
            Vm vm = new VmSimple(mips, pes);
            vm.setRam(ram).setBw(1000).setSize(10000);
            list.add(vm);
        }
    }
}