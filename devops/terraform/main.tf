provider "aws" {
  region = "us-east-1"
}


resource "aws_instance" "win_server_2019" {
  ami                         = "ami-0790368b78dc061cb"
  instance_type               = "t2.small"
  #key_name                    = "my_ubuntu"
  vpc_security_group_ids      = [aws_security_group.sg_win.id]
  subnet_id                   = aws_default_subnet.default_subnet.id
  user_data                   = <<-EOF
                <powershell>
                # Enable WinRM
                # Enable PowerShell remoting
                Enable-PSRemoting -Force

                # Set WinRM service startup type to automatic
                Set-Service WinRM -StartupType 'Automatic'

                # Configure WinRM Service
                Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true
                Set-Item -Path 'WSMan:\localhost\Service\AllowUnencrypted' -Value $true
                Set-Item -Path 'WSMan:\localhost\Service\Auth\Basic' -Value $true
                Set-Item -Path 'WSMan:\localhost\Service\Auth\CredSSP' -Value $true

                # Create a self-signed certificate and set up an HTTPS listener
                # us this one if IMDSv2 is active
                $token = Invoke-RestMethod -Uri http://169.254.169.254/latest/api/token -Method PUT -Headers @{'X-aws-ec2-metadata-token-ttl-seconds'='21600'}
                $hostname = Invoke-RestMethod -Uri http://169.254.169.254/latest/meta-data/public-hostname -Headers @{'X-aws-ec2-metadata-token'=$token}
                $cert = New-SelfSignedCertificate -DnsName $hostname -CertStoreLocation "cert:\LocalMachine\My"

                winrm delete winrm/config/Listener?Address=*+Transport=HTTPS
                winrm create winrm/config/Listener?Address=*+Transport=HTTPS "@{Hostname=`"$($hostname)`";CertificateThumbprint=`"$($cert.Thumbprint)`"}"
                
                # Restart the WinRM service
                Restart-Service WinRM

                # List the WinRM listeners
                winrm enumerate winrm/config/Listener


                # Now test the connection using my linux machine
                # telnet ip address 5986

                # download python file
                Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python-3.10.0-amd64.exe

                # start installation of app
                Start-Process -FilePath "python-3.10.0-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
                
                 # Set Administrator password
                $adminPassword = "MyStrongPassword123!"
                net user Administrator $adminPassword
                
                </powershell>
                EOF
                
                    # $password = ConvertTo-SecureString "XTM-HpMK3vuem*xrktYsAZ4uJTuUDQTU" -AsPlainText -Force
                    # $user = New-Object System.Management.Automation.PSCredential ("Administrator", $password)
  associate_public_ip_address = true
  tags = {
    Name = "Windows Server"
  }


}

resource "aws_default_vpc" "default_vpc" {
}

data "aws_availability_zones" "select_az" {

}
resource "aws_default_subnet" "default_subnet" {
  availability_zone = data.aws_availability_zones.select_az.names[0]
}
resource "aws_security_group" "sg_win" {
  name   = "win_server_sg"
  vpc_id = aws_default_vpc.default_vpc.id

  ingress {
    description = "Allows RDP"
    from_port   = 3389
    to_port     = 3389
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
 ingress {
    description = "Allows WinRM on http"
    from_port   = 5985
    to_port     = 5985
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # HTTP WinRM access
  }
  ingress {
    description = "Allows WinRM on https"
    from_port   = 5986
    to_port     = 5986
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

}

# Output the public IP address of the instance
output "instance_public_ip" {
  value = aws_instance.win_server_2019.public_ip
}

resource "null_resource" "install_resource" {

  # Use the remote-exec provisioner to run a PowerShell script to install Python
  provisioner "remote-exec" {
    inline = [
      "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile C:\\python-installer.exe",
      "Start-Process -FilePath C:\\python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait",
      "Remove-Item C:\\python-installer.exe"
    ]

    # Use WinRM to connect to the Windows instance
    connection {
      type     = "winrm"
      user     = "Administrator"
      password = var.serv_password
      host     = aws_instance.win_server_2019.public_ip
      port     = 5985
    #   https    = true
    #   insecure = true
      timeout  = "5m"
    }
  }

 depends_on = [ aws_instance.win_server_2019 ]
}
