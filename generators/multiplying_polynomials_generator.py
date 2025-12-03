import random
from base_generator import ProblemGenerator
from helpers import step, jid

class MultiplyingPolynomialsGenerator(ProblemGenerator):
    """
    Generates problems for multiplying polynomials (e.g., Binomial * Trinomial).
    (ax + b)(cx^2 + dx + e)
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        # P1 is binomial (deg 1)
        a = random.randint(-5, 5)
        if a == 0: a = 1
        b = random.randint(-5, 5)
        if b == 0: b = 1
        
        # P2 is trinomial (deg 2)
        c = random.randint(-5, 5)
        if c == 0: c = 1
        d = random.randint(-5, 5)
        if d == 0: d = 1
        e = random.randint(-5, 5)
        if e == 0: e = 1
        
        # Format P1
        term_a = f"{a}x" if a != 1 else "x"
        if a == -1: term_a = "-x"
        op_b = "+" if b >= 0 else "-"
        p1_str = f"({term_a} {op_b} {abs(b)})"
        
        # Format P2
        term_c = f"{c}x^2" if c != 1 else "x^2"
        if c == -1: term_c = "-x^2"
        
        op_d = "+" if d >= 0 else "-"
        term_d = f"{abs(d)}x" if abs(d) != 1 else "x"
        
        op_e = "+" if e >= 0 else "-"
        term_e = str(abs(e))
        
        p2_str = f"({term_c} {op_d} {term_d} {op_e} {term_e})"
        
        steps = []
        steps.append(step("POLY_MULT_SETUP", f"{p1_str}{p2_str}"))
        
        # Distribute a*x
        # (ax)(cx^2) + (ax)(dx) + (ax)(e)
        t3_coeff = a * c
        t2_a_coeff = a * d
        t1_a_coeff = a * e
        
        row1_terms = []
        row1_terms.append(f"{t3_coeff}x^3")
        row1_terms.append(f"{t2_a_coeff}x^2" if t2_a_coeff >= 0 else f"{t2_a_coeff}x^2") # sign handling needed for list? 
        # Standardize signs later or in list
        
        # Let's produce the distribution string
        def term_str(coeff, power):
            if coeff >= 0:
                sign = "+"
            else:
                sign = "-"
            val = abs(coeff)
            if power == 3: base = "x^3"
            elif power == 2: base = "x^2"
            elif power == 1: base = "x"
            else: base = ""
            
            return f"{sign} {val}{base}".strip()
            
        dist1_str = f"Distribute {term_a}: "
        dist1_parts = [term_str(t3_coeff, 3), term_str(t2_a_coeff, 2), term_str(t1_a_coeff, 1)]
        # Clean up leading +
        if dist1_parts[0].startswith("+"): dist1_parts[0] = dist1_parts[0][2:]
        steps.append(step("DIST_TERM", term_a, " ".join(dist1_parts)))
        
        # Distribute b
        t2_b_coeff = b * c
        t1_b_coeff = b * d
        t0_coeff = b * e
        
        dist2_parts = [term_str(t2_b_coeff, 2), term_str(t1_b_coeff, 1), term_str(t0_coeff, 0)]
        if dist2_parts[0].startswith("+"): dist2_parts[0] = dist2_parts[0][2:]
        steps.append(step("DIST_TERM", str(b) if b<0 else f"+{b}", " ".join(dist2_parts)))
        
        # Group
        # x^3: t3
        # x^2: t2_a + t2_b
        # x:   t1_a + t1_b
        # c:   t0
        
        final_t3 = t3_coeff
        final_t2 = t2_a_coeff + t2_b_coeff
        final_t1 = t1_a_coeff + t1_b_coeff
        final_t0 = t0_coeff
        
        # Show grouping
        grp_t2 = f"{t2_a_coeff}x^2 {term_str(t2_b_coeff, 2)}"
        grp_t1 = f"{t1_a_coeff}x {term_str(t1_b_coeff, 1)}"
        
        steps.append(step("POLY_GROUP_LIKE", f"{t3_coeff}x^3 + ({grp_t2}) + ({grp_t1}) {term_str(t0_coeff, 0)}"))
        
        # Construct final
        res_parts = [term_str(final_t3, 3), term_str(final_t2, 2), term_str(final_t1, 1), term_str(final_t0, 0)]
        if res_parts[0].startswith("+"): res_parts[0] = res_parts[0][2:]
        
        # Filter out 0 coeffs if not the only term?
        final_terms = []
        for i, val in enumerate([final_t3, final_t2, final_t1, final_t0]):
            if val != 0:
                final_terms.append(res_parts[i])
                
        if not final_terms:
            ans = "0"
        else:
            # Join and fix spacing
            # res_parts already have signs.
            # If first term has sign? handled.
            # But " - 5x^2" is fine. "+ 5x^2" -> "5x^2" at start? handled for first term of original set.
            # But if first term was 0, next term might be "+ 5x^2".
            if final_terms[0].startswith("+"): final_terms[0] = final_terms[0][2:]
            ans = " ".join(final_terms)
            
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="multiply_poly_distribute",
            problem=f"Multiply: {p1_str}{p2_str}",
            steps=steps,
            final_answer=ans
        )
