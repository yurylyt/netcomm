from community import Community
from protocol import Protocol
import time
from session import Session

NITER = 10  # Number of iterations

netcomm = Community(200)
protocol = Protocol(netcomm)
start_time_total = time.time()

print("Running experiments, iterations count: ", NITER)
for istep in range(NITER):
    if istep % 100 == 0:
        print("Done iterations: ", istep)
    start_time = time.time()
    Session(netcomm).simulate()
    session_time = time.time()
    protocol.observe()
    observation_time = time.time()
    print(f"Session: {session_time - start_time}ms, Observation: {observation_time - session_time}ms")
running_time = time.time()


# ----------------------------------------------------------
# store the experiment outcomes
# ----------------------------------------------------------
print(f"Storing the experiment results ({len(protocol.data())})...")
out_file = open("protocol.dat", "w")
for item in protocol.data():
    out_file.write(" ".join(str(w) for w in item.W))
    out_file.write(f" {item.DP} ")
    out_file.write(" ".join(str(w) for w in item.WP))
    out_file.write("\n")

out_file.close()

print(f"Running time: {running_time - start_time_total}ms")