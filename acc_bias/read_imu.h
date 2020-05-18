#include <fstream>
#include <vector>
#include <string>
#include <stdlib.h>
#include <iostream>
struct XYZ
{
    double x, y, z;
};

int imu_reader(const char *imu_file, std::vector<double> &stamps, std::vector<XYZ> &grys, std::vector<XYZ> &accs)
{
    // std::cout << imu_file << std::endl;
    std::ifstream imu;
    imu.open(imu_file);
    if (!imu.is_open())
    {
        std::cout << "open err\n";
        return -1;
    }
    XYZ xyz;
    while (!imu.eof())
    {
        std::string line;
        imu >> line;
        // std::cout << line << std::endl;
        std::vector<double> datas;

        double data = 0;
        char c[256];
        double stamp = 0;
        int j = 0;
        int i = 0;
        for (; i < line.length(); i++)
        {
            if (line[i] == ',')
            {
                if (stamp < 1e-6)
                {
                    long stp = atol(c);
                    stamp = stp / 1e9;
                    data = stamp;
                    datas.push_back(data);
                    j = 0;
                }
                else
                {
                    data = atof(c);
                    datas.push_back(data);
                    j = 0;
                }
            }
            else
            {
                c[j] = line[i];
                j++;
                c[j] = '\0';
            }
        }
        data = atof(c);
        datas.push_back(data);

        // for (size_t i = 0; i < datas.size(); i++)
        // {
        //     std::cout << datas[i] << "\t";
        // }
        // std::cout << "\n";

        if (datas.size() == 7)
        {
            stamps.push_back(datas[0]);
            xyz.x = datas[1];
            xyz.y = datas[2];
            xyz.z = datas[3];
            grys.push_back(xyz);
            xyz.x = datas[4];
            xyz.y = datas[5];
            xyz.z = datas[6];
            accs.push_back(xyz);
        }
    }

    return 0;
}