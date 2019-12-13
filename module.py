def summator(v1, v2):
  return v1 + v2

def amplifier(v1,k):
  return v1*k

def inertional(v1, w_prev, t):
  return (v1 + w_prev*t) / (1 + t)

def integrator(v1, w_prev):
  return 0.001*v1 + w_prev

def real_differential(v1, v_prev, w_prev, t):
  return (w_prev*t + v1 - v_prev) / (1 + t)

def dampfer(v1, v_prev, w_prev, t1, t2):
  return (w_prev*t1 + v1*(1 + t2) - t2*v_prev) / (1 + t1)

