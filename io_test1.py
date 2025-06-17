import serial
import time
import argparse
import sys
from virtual import VirtualPort



class SerialCommandSender:
    def __init__(self, port, baudrate=115200, timeout=1):
        """Initialize serial connection."""
        if port =='COM3':
            self.ser = VirtualPort()
        else:
            try:
                
                    self.ser = serial.Serial(
                        port=port,
                        baudrate=baudrate,
                        timeout=timeout,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE
                    )
            except serial.SerialException as e:
                print(f"Error opening serial port {port}: {e}")
                sys.exit(1)

    def get_response(self):
        """Wait for and collect response."""
        response = ""
        while True:
            if self.ser.in_waiting:
                char = self.ser.read().decode(errors='ignore')
                if '>' in char:  # Command prompt indicates end of response
                    break
                response += char
            time.sleep(0.0001)  # Small delay to prevent CPU hogging
        print(f"{response.strip()}\r\n")
        return response
        
    def send_command(self, command):
        """Send command and wait for response."""
        # Replace spaces with hyphens
        command = command.replace(' ', '-')
        
        # Add newline to command
        command = command + '\r\n'
        
        # Send command
        print(f"{command.strip().replace('-', ' ')}")
        self.ser.write(command.encode())
        self.get_response()

    def execute_commands(self, commands):
        """Execute a list of commands."""
        for command in commands:
            self.send_command(command)

    def process_file(self, filename):
        """Process command file and send commands."""
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Skip empty lines
                if not line:
                    i += 1
                    continue
                
                # Handle comment lines
                comment_pos = line.find('#')
                if comment_pos != -1:
                    if comment_pos == 0:
                        print(">> ", line[comment_pos+1:])
                    line = line[:comment_pos].strip()
                    if not line:  # Skip if line only contained comment
                        i += 1
                        continue

                # Check for loop start
                if line.startswith('LOOP '):
                    try:
                        iteration_count = int(line.split()[1])
                        loop_commands = []
                        i += 1
                        
                        # Collect commands until LOOP END
                        while i < len(lines):
                            loop_line = lines[i].strip()
                            
                            # Handle comments in loop
                            comment_pos = loop_line.find('#')
                            if comment_pos != -1:
                                if comment_pos == 0:
                                    print(">> ", loop_line[comment_pos+1:])
                                loop_line = loop_line[:comment_pos].strip()
                                
                            if loop_line == 'LOOP END':
                                break
                            elif loop_line:  # Add non-empty lines to loop commands
                                loop_commands.append(loop_line)
                            i += 1
                            
                        if i >= len(lines):
                            raise ValueError("LOOP END not found")
                            
                        # Execute the loop
                        print(f">> Starting loop with {iteration_count} iterations")
                        for iteration in range(iteration_count):
                            print(f">> Iteration {iteration + 1}/{iteration_count}")
                            self.execute_commands(loop_commands)
                        print(">> Loop completed")
                            
                    except (ValueError, IndexError) as e:
                        print(f"Error in loop syntax: {e}")
                        
                else:
                    # Process normal command
                    self.send_command(line)
                    
                i += 1
                    
        except Exception as e:
            print(f"Error: {e}")

    def close(self):
        """Close serial connection."""
        if self.ser.is_open:
            self.ser.close()

def main():
    parser = argparse.ArgumentParser(description='Send commands from file to serial port.')
    parser.add_argument('port', help='Serial port name (e.g., COM1 or /dev/ttyUSB0)')
    parser.add_argument('file', help='Command file to process')
    parser.add_argument('--baudrate', type=int, default=115200, help='Baudrate (default: 115200)')
    parser.add_argument('--timeout', type=float, default=1.0, help='Serial timeout in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    sender = None
    try:
        sender = SerialCommandSender(args.port, args.baudrate, args.timeout)
        # Get App version
        sender.send_command('V')
        sender.process_file(args.file)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sender:
            sender.close()

if __name__ == "__main__":
    main()




   