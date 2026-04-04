import org.cloudsimplus.core.CloudSimPlus;
import org.cloudsimplus.datacenters.DatacenterSimple;
import org.cloudsimplus.hosts.HostSimple;
import org.cloudsimplus.resources.Pe;
import org.cloudsimplus.resources.PeSimple;
import org.cloudsimplus.vms.VmSimple;
import org.cloudsimplus.brokers.DatacenterBrokerSimple;

import java.util.ArrayList;
import java.util.List;

public class ValidationTest {
    public static void main(String[] args) {
        CloudSimPlus simulation = new CloudSimPlus();

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

        List<HostSimple> hosts = List.of(host);

        DatacenterSimple dc =
            new DatacenterSimple(simulation, hosts);

        DatacenterBrokerSimple broker =
            new DatacenterBrokerSimple(simulation);

        VmSimple vm = new VmSimple(1000, 2);
        vm.setRam(2048).setBw(1000).setSize(10000);

        broker.submitVm(vm);

        simulation.start();

        System.out.println("CloudSim validation completed");
    }
}