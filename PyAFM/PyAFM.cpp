#include <iostream>
#include <fstream>
#include <math.h>

#define POINTS 2048 // Number of points to be ploted


void getAMWave(float carrier_frequency, float am_frequency, float amplitude, float depth,float* wave, float dt)
{
    /// This function creates an AM wave according to the parameters
    /// and stores it into the wave vector

    float s; // wave value in a given time
    float pi = M_PI;

    for(int i = 0; i < POINTS; i++) // calculates the AM wave's value and store it into wave
    {
        s = amplitude * (1 + depth * sin(2 * pi * am_frequency * dt * i));
        float aux = 2 * pi * carrier_frequency * dt * i;
        s = s * sin(aux);
        aux = 1 + pow(depth, 2) / 2;
        aux = sqrt(aux);
        s /= aux;
        wave[i] = s;
    }
}
void getFMWave(float carrier_frequency, float fm_frequency, float amplitude, float depth, float* wave, float dt)
{
    /// This function creates an FM wave according to the parameters
    /// and stores it into the wave vector

    float s; // wave value in a given time
    float pi = M_PI;

    for(int i = 0; i < POINTS; i++) // calculates the FM wave's value and store it into wave
    {
        s = 2 * pi * carrier_frequency * dt * i;
        s += ((depth * fm_frequency) / (2 * fm_frequency) * sin(2 * pi * fm_frequency * dt * i));
        s = sin(s);
        s = amplitude * s;
        wave[i] = s;
    }
}

int main()
{
    /// This function will be erased in a near future,
    /// for now, it is used to test the AM and FM functions output

    std::ofstream file1;
    std::ofstream file2;
    file1.open("am.dat"); // create a am.dat file if its not created yet
    file2.open("fm.dat"); // create a fm.dat file if its not created yet
    float wave[POINTS], dt = 0.0001; // initialize the wave's values buffer and set delta time
    getAMWave(60, 10, 2, .5, wave, dt); // call getAMWave to test the output
    for(int i = 0; i < POINTS; i++) // write the wave buffer to file1
    {
        file1 << i * dt << "    " << wave[i] << std::endl;
    }
    getFMWave(100, 40, 2, .75, wave, dt); // call getFMWave to test the output
    for(int i = 0; i < POINTS; i++) // write the wave buffer to file2
    {
        file2 << i * dt << "    " << wave[i] << std::endl;
    }
    return 0;
}
