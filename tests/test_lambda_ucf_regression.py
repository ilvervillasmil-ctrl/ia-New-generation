import math

def test_lambda_ucf_value_and_error_regression():
    """
    Regression test for the UCF cosmological constant ansatz:
        Lambda_Omega = beta^(27*pi + beta*phi^2)
    Validates:
      - exponent numerical value
      - Lambda numerical value
      - relative error vs frozen anchor (2.888e-122) stays ~2.7%
    """
    beta = 1.0 / 27.0
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    exponent = 27.0 * math.pi + beta * (phi ** 2)

    # Reference numbers stated in your paper/report
    exponent_ref = 84.919965
    lambda_ref = 2.8096e-122
    lambda_obs_anchor = 2.8880e-122  # frozen observational anchor used in report
    expected_rel_err = 0.02716       # ~2.716%

    Lambda = beta ** exponent
    rel_err = abs(Lambda - lambda_obs_anchor) / lambda_obs_anchor

    # Tight enough to catch accidental changes, loose enough for float noise
    assert abs(exponent - exponent_ref) < 5e-6
    assert abs(Lambda - lambda_ref) / lambda_ref < 5e-4
    assert abs(rel_err - expected_rel_err) < 5e-4
