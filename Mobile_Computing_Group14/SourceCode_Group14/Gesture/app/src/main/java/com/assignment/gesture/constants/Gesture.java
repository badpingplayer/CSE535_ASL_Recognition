package com.assignment.gesture.constants;

import java.io.Serializable;
import java.util.Arrays;
import java.util.List;

public enum Gesture implements Serializable {
    H0("ACPower"),
    H1("Algorithm"),
    H2("Antenna"),
    H3("Authentication"),
    H4("Authorization"),
    H5("Bandwidth"),
    H6("Bluetooth"),
    H7("Browser"),
    H8("Cloudcomputing"),
    H9("GDataCompression"),
    H10("DataLinkLayer"),
    H11("DataMining"),
    H12("Decryption"),
    H13("Domain"),
    H14("Email"),
    H15("Exposure"),
    H16("Filter"),
    H17("Firewall"),
    H18("Flooding"),
    H19("Gateway"),
    H20("Hacker"),
    H21("Header"),
    H22("HotSwap"),
    H23("Hyperlink"),
    H24("Infrastructure"),
    H25("Integrity"),
    H26("Internet"),
    H27("Intranet"),
    H28("Latency"),
    H29("Loopback"),
    H30("Motherboard"),
    H31("Network"),
    H32("Networking"),
    H33("Networklayer"),
    H34("Node"),
    H35("Packet"),
    H36("Partition"),
    H37("PasswordSniffing"),
    H38("Patch"),
    H39("Phishing"),
    H40("PhysicallLayer"),
    H41("Ping"),
    H42("Portscan"),
    H43("PresentationalLayer"),
    H44("Protocol");

    private String gesture;

    Gesture(String gesture) {
        this.gesture = gesture;
    }

    public static Gesture getGesture(String gesture) {
        for (Gesture g : Gesture.values()) {
            if (g.getGesture().equals(gesture)) {
                return g;
            }
        }
        return null;
    }

    public static List<Gesture> getGestures() {
        return Arrays.asList(Gesture.values());
    }

    public String getGesture() {
        return gesture;
    }
}
