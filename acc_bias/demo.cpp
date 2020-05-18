#include "imu_cal.h"
#include "read_imu.h"
using namespace std;
int main(int argc, char **argv)
{
    string fun(argv[1]);
    string path(argv[2]);
    cout << fun << endl;
    cout << path << endl;
    // string path = "/home/hi/workspace/cppcode/testQuaternion/imu0.csv";
    if (fun == "1")
    {
        // string path(argv[1]);
        // cout<<"a\n";
        std::vector<XYZ> grys;
        std::vector<XYZ> accs;
        std::vector<double> stamps;
        if (imu_reader(path.c_str(), stamps, grys, accs) < 0)
            return -1;
        // cout<<"b\n";

        std::vector<ImuSample> accSamples(accs.size());
        for (size_t i = 0; i < accs.size(); i++)
        {
            accSamples[i].accel[0] = accs[i].x;
            accSamples[i].accel[1] = accs[i].y;
            accSamples[i].accel[2] = accs[i].z;
        }
        int ret = (int)(checkImuData(accSamples.data(), accSamples.size()));
        cout << ret << endl;
        return ret;
    }
    if (fun == "2")
    {

        // string name[6] = { "imu_you.csv", "imu_zuo.csv", "imu_shang.csv", "imu_xia.csv","imu_qian.csv","imu_hou.csv"};
        // string name[6] = {"imu_D.csv", "imu_U.csv", "imu_D.csv", "imu_U.csv", "imu_D.csv", "imu_U.csv"};
        // string name[6] = {"imu_hou.csv", "imu_qian.csv", "imu_shang.csv", "imu_xia.csv", "imu_you.csv", "imu_zuo.csv"};
        string name[6] = {"imu_R.csv", "imu_L.csv", "imu_D.csv", "imu_U.csv", "imu_F.csv", "imu_B.csv"};
        // string path(argv[1]);
        if (path[path.length() - 1] != '/')
        {
            path += "/";
        }

        for (size_t i = 1; i < 7; i++)
        {

            std::vector<XYZ> grys;
            std::vector<XYZ> accs;
            std::vector<double> stamps;
            if (imu_reader((path + name[i - 1]).c_str(), stamps, grys, accs) < 0)
                return -1;
            std::vector<ImuSample> accSamples(accs.size());
            for (size_t i = 0; i < accs.size(); i++)
            {
                // if (i<2)
                //     cout<<accs[i].x<<"\t"<<accs[i].y<<"\t"<<accs[i].z<<endl;
                accSamples[i].accel[0] = accs[i].x;
                accSamples[i].accel[1] = accs[i].y;
                accSamples[i].accel[2] = accs[i].z;
            }
            char result[256];
            // std::cout << i << "\t" << (int)(CalculateAccMean(accSamples.data(), accSamples.size(), i, result)) << endl;
            // cout << string(result) << endl;
            int ret = (int)(CalculateAccMean(accSamples.data(), accSamples.size(), i, result));
    
            std::cout << i << "\t" << ret << endl;
            cout << string(result) << endl;

            if (i == 6)
            {
                if (ret == 0)
                {
                    ofstream of;
                    of.open("AccelBias.txt");
                    of << result;
                    of.close();
                }

                return ret;
            }
        }
    }

    return 0;
}