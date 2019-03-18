import java.awt.AWTException;
import java.awt.Robot;
import java.util.concurrent.TimeUnit;
import java.io.*;
import java.net.*;
import javax.swing.FocusManager;
import java.awt.Toolkit;
import java.awt.Dimension;

public class UdpClient {
    public static void main(String[] args) throws IOException, AWTException, InterruptedException {
        Robot rob = new Robot();
        int PORT = 5005;

        //InetAdress ip = "0.0.0.0";

        DatagramSocket serverSocket = new DatagramSocket(null);
        InetSocketAddress address = new InetSocketAddress("0.0.0.0", PORT);
        serverSocket.bind(address);

        byte[] receiveData = new byte[1024];
        
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        double screen_width = screenSize.getWidth();
        double screen_height = screenSize.getHeight();

        while (true) {
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            serverSocket.receive(receivePacket);
            String sentence = new String(receivePacket.getData());
            String[] parts = sentence.split(" ");

            String new_y = "";

            for(int i=0; i<parts[1].length(); i++){
                if((int)parts[1].charAt(i) > 0){
                    new_y += parts[1].charAt(i);
                }else {
                    break;
                }
            }
            

            double x = Double.parseDouble(parts[0]);
            double y = Double.parseDouble(new_y);


            x = x*screen_width;
            y = y*screen_height;

            int x_pos = (int) Math.round(x);
            int y_pos = (int) Math.round(y);
            rob.mouseMove(x_pos, y_pos);

        }
    }
}
