#ifndef NEW_G2_IMU_CAL__
#define NEW_G2_IMU_CAL__
#define IMU_CAL_INTERFACE_EXPORT __attribute__ ((visibility("default")))
struct ImuSample
{
    float accel[3];
};

enum imuCal_CODE
{
    cal_SUCCESS = 0,
    cal_VARIANCE_EXCEEDED = 1,
    cal_ZERO_VARIANCE,
    cal_HIGH_BIAS
};

/**
 * @brief check the quality of accel data samples.
 * @param[in] samples   pointer of data samples array
 * @param[in] len   length of the samples array
 * @return cal_SUCCESS if OK, other values if failed
 */
IMU_CAL_INTERFACE_EXPORT imuCal_CODE checkImuData(ImuSample *samples,int len);
/**
 * @brief check the quality of accel data samples.
 * @param[in] samples   pointer of data samples array
 * @param[in] len   length of the samples array
 * @param[in] step   means the data we are processing is from which face
 * @param[in] result    pointer of the Imu Calibration result, save the data into calibration file. Please define an array of 200 length such as result[200],and deliver the array pointer to the function
 * @return cal_SUCCESS if OK, other values if failed
 */
IMU_CAL_INTERFACE_EXPORT imuCal_CODE CalculateAccMean(ImuSample *samples,int len,int step,char *result);
#endif