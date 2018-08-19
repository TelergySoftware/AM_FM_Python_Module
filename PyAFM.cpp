#include <iostream>
#include <fstream>
#include <math.h>

#define POINTS 2048


void getAMWave(float carrier_frequency, float am_frequency, float amplitude, float depth,float* wave, float dt)
{
    float s;
    float pi = M_PI;

    for(int i = 0; i < POINTS; i++)
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
    float s;
    float pi = M_PI;

    for(int i = 0; i < POINTS; i++)
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
    std::ofstream file1;
    std::ofstream file2;
    file1.open("am.dat");
    file2.open("fm.dat");
    float wave[POINTS], dt = 0.0001;
    getAMWave(60, 10, 2, .5, wave, dt);
    for(int i = 0; i < POINTS; i++)
    {
        file1 << i * dt << "    " << wave[i] << std::endl;
    }
    getFMWave(100, 40, 2, .75, wave, dt);
    for(int i = 0; i < POINTS; i++)
    {
        file2 << i * dt << "    " << wave[i] << std::endl;
    }
    return 0;
}
