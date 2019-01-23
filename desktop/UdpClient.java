import java.awt.AWTException; 
import java.awt.Robot;
import java.util.concurrent.TimeUnit;
import java.io.*; 
import java.net.*;

public class UdpClient {
    public static void main(String[] args) throws IOException, AWTException, InterruptedException {
        System.out.println("TEST");
        Robot rob = new Robot();
        // for(int i=20; i<200; i++){
        //     rob.mouseMove(i,20);
        //     System.out.println(i);
        //     TimeUnit.MILLISECONDS.sleep(100);
        // }

        int PORT = 5005;
        DatagramSocket serverSocket = new DatagramSocket(PORT, AF_INET);
        byte[] receiveData = new byte[1024];
        byte[] sendData = new byte[1024];

        while(true) {
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            serverSocket.receive(receivePacket);
            String sentence = new String( receivePacket.getData());
            System.out.println("RECEIVED: " + sentence);
        }
}
    }
}