🔍Port Scanner

A fast and efficient multi-threaded port scanner built in Python. This tool scans a target host for open ports, detects running services, attempts basic banner grabbing, and exports results to a CSV file for further analysis.

✨ Features

🚀 Multithreaded scanning (default: 100 threads, customizable)

🌍 Hostname resolution → automatically resolves domain names to IP addresses

🔎 Open port detection → checks port availability with socket connections

🛠 Service detection → identifies common services using socket.getservbyport()

📜 Banner grabbing → collects service banners when available

📊 Detailed scan results → displays open ports, detected services, and banners

💾 CSV export → saves scan results with timestamps for easy reporting

⏱ Performance tracking → shows total scan time and number of open ports

🖥️ Installation

Clone the repository and navigate into the project folder:

git clone https://github.com/Haritha-official/Port_Scanner.git

No external dependencies are required (only Python standard library).

▶️ Usage
You will be prompted to enter:

Host (domain name or IP)

Start port

End port

Number of threads (default: 100)
