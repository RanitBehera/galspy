import galspy.IO.MPGadget as mp
import galspy.utility.visualization as vis

root = mp.RSGRoot("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017").RKSParticles

ihid = root.InternalHaloID.ReadBlob("000004")
ppos = root.Position.ReadBlob("000004")

# print(ihid[12070:12070+23960])

ippos = ppos[12070:12070+23960]

cv = vis.CubeVisualizer()
cv.add_points(ippos)
cv.show()