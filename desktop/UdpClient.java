import java.awt.AWTException;
import java.awt.Robot;
import java.util.concurrent.TimeUnit;
import java.io.*;
import java.net.*;
import javax.swing.FocusManager;

public class UdpClient {
    public static void main(String[] args) throws IOException, AWTException, InterruptedException {
        System.out.println("TEST");
        Robot rob = new Robot();
        // for(int i=20; i<200; i++){

        // System.out.println(i);
        // TimeUnit.MILLISECONDS.sleep(100);
        // }
        int PORT = 5005;
        DatagramSocket serverSocket = new DatagramSocket(PORT);
        byte[] receiveData = new byte[1024];
        while (true) {
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            serverSocket.receive(receivePacket);
            String sentence = new String(receivePacket.getData());
            String[] parts = sentence.split(" ");
            Integer x = Integer.parseInt(parts[0]);
            Integer y = Integer.parseInt(parts[1].substring(0, parts[1].length() - 1019));
            rob.mouseMove(x, y);
        }
    }
}
