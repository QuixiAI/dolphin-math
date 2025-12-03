import random
from base_generator import ProblemGenerator
from helpers import step, jid

class PolynomialAddSubGenerator(ProblemGenerator):
    """
    Generates problems for adding and subtracting polynomials.
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        op = random.choice(['+', '-'])
        op_name = "add" if op == '+' else "subtract"
        
        # Degree of polynomials
        deg1 = random.randint(1, 3)
        deg2 = random.randint(1, 3)
        
        # Generate coeffs: index i is x^i
        # Let's use dictionary {power: coeff} for sparse handling
        
        def gen_poly(degree):
            poly = {}
            for i in range(degree + 1):
                if random.random() < 0.8: # 80% chance of term
                    c = random.randint(-9, 9)
                    if c != 0: poly[i] = c
            # Ensure highest degree exists
            if degree not in poly:
                c = random.randint(1, 9) * random.choice([-1, 1])
                poly[degree] = c
            return poly
            
        p1 = gen_poly(deg1)
        p2 = gen_poly(deg2)
        
        # Helper to format poly
        def fmt_poly(p):
            terms = []
            degrees = sorted(p.keys(), reverse=True)
            for d in degrees:
                c = p[d]
                if c == 0: continue
                
                # Sign
                if not terms: # First term
                    sign = "-" if c < 0 else ""
                else:
                    sign = "- " if c < 0 else "+ "
                    
                val = abs(c)
                val_str = str(val)
                if val == 1 and d > 0: val_str = ""
                
                if d == 0:
                    term = f"{sign}{val}"
                elif d == 1:
                    term = f"{sign}{val_str}x"
                else:
                    term = f"{sign}{val_str}x^{d}"
                terms.append(term)
            return " ".join(terms) if terms else "0"
            
        p1_str = fmt_poly(p1)
        p2_str = fmt_poly(p2)
        
        problem_str = f"({p1_str}) {op} ({p2_str})"
        
        steps = []
        steps.append(step("POLY_SETUP", problem_str))
        
        # Step 1: Remove parentheses / Distribute negative
        if op == '-':
            # Flip signs of p2
            p2_neg = {d: -c for d, c in p2.items()}
            p2_fmt = fmt_poly(p2_neg)
            
            # Show rewrite
            # Need to handle signs correctly in join. 
            # If p2_fmt starts with -, use space?
            # Easiest: just list terms.
            steps.append(step("POLY_DIST_NEG", f"Distribute negative sign to second polynomial"))
            # Just show the list of terms to combine?
            # Or rewrite expression: p1_str + p2_neg_str (handling signs)
            # Let's jump to grouping logic which is clearer
            
        # Step 2: Group Like Terms
        all_degrees = sorted(list(set(p1.keys()) | set(p2.keys())), reverse=True)
        
        grouped_terms_display = []
        final_poly = {}
        
        for d in all_degrees:
            c1 = p1.get(d, 0)
            c2 = p2.get(d, 0)
            
            # If subtract, subtract c2
            eff_c2 = c2 if op == '+' else -c2
            
            final_c = c1 + eff_c2
            if final_c != 0:
                final_poly[d] = final_c
                
            # Formatting the group
            # (2x^2 - 5x^2)
            if c1 == 0 and c2 == 0: continue
            
            terms_in_group = []
            if c1 != 0:
                terms_in_group.append(f"{c1}x^{d}" if d > 1 else (f"{c1}x" if d==1 else f"{c1}"))
            if c2 != 0:
                # Show original sign relative to op?
                # If op is -, we are doing (c1 - c2)
                # Display: (c1x^2 - c2x^2)
                
                # Simpler: just use effective values
                val1_str = f"{c1}x^{d}" if d>1 else (f"{c1}x" if d==1 else f"{c1}")
                val2_str = f"{eff_c2}x^{d}" if d>1 else (f"{eff_c2}x" if d==1 else f"{eff_c2}")
                
                # Make coeff explicit sign for second term
                if eff_c2 >= 0: val2_str = "+" + val2_str
                
                if c1 == 0: 
                    grp = f"({val2_str.replace('+','',1)})" # remove leading +
                else:
                    grp = f"({val1_str} {val2_str})"
                grouped_terms_display.append(grp)
            elif c1 != 0:
                 # Only c1
                 grp = f"({c1}x^{d})" if d>1 else (f"({c1}x)" if d==1 else f"({c1})")
                 grouped_terms_display.append(grp)
                 
        group_str = " + ".join(grouped_terms_display)
        steps.append(step("POLY_GROUP_LIKE", group_str.replace(" + -", " - ")))
        
        # Step 3: Combine
        ans = fmt_poly(final_poly)
        steps.append(step("POLY_COMBINE", ans))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="polynomial_add_sub",
            problem=problem_str,
            steps=steps,
            final_answer=ans
        )
