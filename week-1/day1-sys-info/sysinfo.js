const os = require("os"); // built-in node module - gives OS info

const { execSync } = require("child_process"); // allows running Linux commands in Node
// execSync -> runs command synchronously

const fs = require("fs"); // file system module - read/write files

const hostname = os.hostname(); // returns hostname

const diskSpace = execSync("df -BG --output=avail / | tail -1") // prints available free sapce in disk in GB
  .toString()
  .trim();

/*
df -> disk free

-BG -> output in GB

--output=avail -> only available space

/ -> root filesystem

tail -1 -> last line(actual value)
*/

const openPorts = execSync(
  "lsof -i -P -n | grep LISTEN | head -5"
).toString();
/*
-i → internet connections

-P → show port numbers

-n → no DNS lookup

grep LISTEN → listening ports

head -5 → top 5
*/

const gateway = execSync(
  "ip route | grep default | awk '{print $3}'"
).toString().trim();
/*
ip route → routing table

grep default → default route

awk '{print $3}' → extract gateway IP
*/

const usersCount = execSync("who | wc -l") // no. of logged in users along with their name
  .toString()
  .trim();
/*
who -> logged-in users

wc -l -> count lines
*/

console.log("Hostname:", hostname);
console.log("Available Disk Space:", diskSpace);
console.log("Open Ports (Top 5):\n", openPorts);
console.log("Default Gateway:", gateway);
console.log("Logged-in Users:", usersCount);

// console -> prints data to terminal

const metrics = {
  cpuUsage: process.cpuUsage(), // CPU time used by node process(micro seconds)
  resourceUsage: process.resourceUsage(), // memory, file reads, context switches
  timestamp: new Date().toISOString() // ISO standard time format
};

fs.writeFileSync( // writes json data to file, sync - data saved before exit
  "logs/day1-sysmetrics.json",
  JSON.stringify(metrics, null, 2)
);

/*
to run script - 
-> node sysinfo.js    (starts node runtime, executes script)
->  cat logs/day1-sysmetrics.json     (cat : displays file content)
*/