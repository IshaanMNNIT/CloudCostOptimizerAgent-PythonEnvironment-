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

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class StressValidationTest {
    public static void main(String[] args) throws Exception {
        CloudSimPlus simulation = new CloudSimPlus();

        // -----------------------------
        // Datacenter setup
        // -----------------------------
        List<HostSimple> hostList = new ArrayList<>();

        for (int h = 0; h < 3; h++) {
            List<Pe> peList = new ArrayList<>();

            for (int i = 0; i < 4; i++) {
                peList.add(new PeSimple(1000));
            }

            HostSimple host = new HostSimple(
                8192,
                10000,
                1000000,
                peList
            );

            hostList.add(host);
        }

        DatacenterSimple datacenter =
            new DatacenterSimple(simulation, hostList);

        DatacenterBrokerSimple broker =
            new DatacenterBrokerSimple(simulation);

        // -----------------------------
        // Read PPO action trace
        // -----------------------------
        List<String> actions = Files.readAllLines(
            Paths.get("actions.txt")
        );

        int smallVmCount = 2;
        int mediumVmCount = 0;
        int largeVmCount = 0;

        // -----------------------------
        // Replay PPO actions
        // -----------------------------
        for (String line : actions) {
            int action = Integer.parseInt(line.trim());

            switch (action) {
                case 0:
                    break;

                case 1:
                    smallVmCount++;
                    break;

                case 2:
                    mediumVmCount++;
                    break;

                case 3:
                    largeVmCount++;
                    break;

                case 4:
                    smallVmCount =
                        Math.max(1, smallVmCount - 1);
                    break;

                case 5:
                    mediumVmCount =
                        Math.max(0, mediumVmCount - 1);
                    break;

                case 6:
                    largeVmCount =
                        Math.max(0, largeVmCount - 1);
                    break;
            }
        }

        // -----------------------------
        // Create VMs from replayed state
        // -----------------------------
        List<Vm> vmList = new ArrayList<>();

        for (int i = 0; i < smallVmCount; i++) {
            Vm vm = new VmSimple(1000, 1);
            vm.setRam(2048)
              .setBw(1000)
              .setSize(10000);
            vmList.add(vm);
        }

        for (int i = 0; i < mediumVmCount; i++) {
            Vm vm = new VmSimple(1500, 2);
            vm.setRam(4096)
              .setBw(1500)
              .setSize(15000);
            vmList.add(vm);
        }

        for (int i = 0; i < largeVmCount; i++) {
            Vm vm = new VmSimple(2000, 4);
            vm.setRam(8192)
              .setBw(2000)
              .setSize(20000);
            vmList.add(vm);
        }

        broker.submitVmList(vmList);

        // -----------------------------
        // Stress workload
        // -----------------------------
        List<Cloudlet> cloudletList = new ArrayList<>();

        for (int i = 0; i < 30; i++) {
            long length;

            if (i >= 15 && i <= 25) {
                length = 12000;
            } else if (i >= 35 && i <= 40) {
                length = 18000;
            } else {
                length = 4000;
            }

            Cloudlet cloudlet = new CloudletSimple(
                length,
                2,
                new UtilizationModelDynamic(0.6)
            );

            cloudlet.setSizes(512);
            cloudletList.add(cloudlet);
        }

        broker.submitCloudletList(cloudletList);

        // -----------------------------
        // Run simulation
        // -----------------------------
        simulation.start();

        // -----------------------------
        // Metrics
        // -----------------------------
        int totalCapacity =
            (smallVmCount * 100) +
            (mediumVmCount * 250) +
            (largeVmCount * 500);

        double avgFinishTime = broker
            .getCloudletFinishedList()
            .stream()
            .mapToDouble(Cloudlet::getFinishTime)
            .average()
            .orElse(0);

        System.out.println("========================================");
        System.out.println("PPO + CLOUDSIM STRESS VALIDATION");
        System.out.println("========================================");
        System.out.println("Small VMs      : " + smallVmCount);
        System.out.println("Medium VMs     : " + mediumVmCount);
        System.out.println("Large VMs      : " + largeVmCount);
        System.out.println("Total Capacity : " + totalCapacity);
        System.out.println(
            "Finished Jobs  : "
            + broker.getCloudletFinishedList().size()
        );
        System.out.println(
            "Avg Finish Time: "
            + avgFinishTime
        );
        System.out.println("========================================");
    }
}