#include <iostream>
#include <vector>
#include <iomanip>
#include <cmath>

enum Month
{
    JAN = 1,
    FEB,
    MAR,
    APR,
    MAY,
    JUN,
    JUL,
    AUG,
    SEP,
    OCT,
    NOV,
    DEC
};

const int days_in_month[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

bool isLeapYear(int year) { return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0); }

int getDays(Month m, bool leap = false)
{
    if (m == FEB && leap)
    {
        return 29;
    }
    return days_in_month[m];
}

struct Record
{
    double date;
    int position;
};

int dateToDay(double date, int year = 2025)
{
    int month = static_cast<int>(date);
    int day = static_cast<int>((date - month) * 100 + 0.5);

    bool leap = isLeapYear(year);
    int totalDays = 0;
    for (int m = 1; m < month; ++m)
    {
        totalDays += getDays(static_cast<Month>(m), leap);
    }

    totalDays += day;
    return totalDays;
}

void linearFit(const std::vector<Record>& data, double& a, double& b)
{
    int n = data.size();
    if (n < 2)
    {
        std::cerr << "Insufficient data, at least two points are needed to fit." << std::endl;
        return;
    }

    double base_day = dateToDay(data[0].date);  // 第一个日期设为 day 0

    double sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

    for (const auto& r : data)
    {
        double x = dateToDay(r.date) - base_day;  // 相对天数
        double y = r.position;

        std::cout << "date: " << r.date << ", days since start: " << x << std::endl;
        std::cout << "rank: " << y << std::endl;

        sumX += x;
        sumY += y;
        sumXY += x * y;
        sumX2 += x * x;
    }

    a = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    b = (sumY - a * sumX) / n;

    std::cout << "Linear fitting results:y = " << a << " * (days since start) + " << b << std::endl;
}

double solveForZero(double a, double b)
{
    if (a == 0)
    {
        throw std::runtime_error("The slope a cannot be 0 (otherwise the line would be horizontal and have no intersection)");
    }
    return -b / a;
}

int main()
{
    std::vector<Record> data = {{7.23, 2016}, {7.30, 1974}, {8.02, 1967}, {8.07, 1947}, {8.08, 1940}, {8.09, 1930}, {9.05, 1777}};

    double a, b;
    linearFit(data, a, b);

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Linear fitting formula: Rank ≈ " << a << " * Days + " << b << std::endl;
    try
    {
        double zeroPoint = solveForZero(a, b);
        std::cout << "The zero point (where Rank = 0) occurs at " << zeroPoint << " days." << std::endl;
    }
    catch (const std::runtime_error& e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
