"""Beta & Correlation tests"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.portfolio_exposure.beta_calculator import calc_beta
from zmatrix.portfolio_exposure.correlation_calculator import calc_correlation

def test_calc_beta():
    stock = [45,46,47,48,47,46,50,52,51,50,53,55,54,56,58]*5
    index = [3000,3010,3020,3015,3025,3030,3040,3050,3060,3070]*8
    b = calc_beta(stock, index)
    assert b is not None
    print(f"✅ beta={b}")

def test_calc_correlation():
    a = [45,46,48,50,49,51]*10
    b = [45,46,47,49,48,50]*10
    c = calc_correlation(a, b)
    assert c is not None
    print(f"✅ corr={c}")

if __name__ == "__main__":
    test_calc_beta()
    test_calc_correlation()
    print("\n🏁 Beta/Corr PASS")
