import random

from base_generator import ProblemGenerator
from helpers import step, jid


def allocation_text(x11, x12, x21, x22):
    return f"x11={x11}, x12={x12}, x21={x21}, x22={x22}"


def cost_terms(allocations, costs):
    return [allocation * cost for allocation, cost in zip(allocations, costs)]


class TransportationGenerator(ProblemGenerator):
    """
    Northwest-corner transportation start and one stepping-stone improvement.

    Op-codes used:
    - TRANSPORT_SETUP: supplies, demands, and costs
    - NW_ALLOC: northwest-corner allocation
    - COST: objective cost phase
    - STEPPING_STONE: empty cell and improvement cycle
    - THETA: limiting shipment adjustment
    - A / S / M (established/shared): exact arithmetic
    - CHECK: improvement and balanced totals
    - Z: initial cost, improved allocation, final cost
    """

    def generate(self) -> dict:
        while True:
            d1 = random.randint(5, 20)
            s1 = random.randint(d1 + 1, d1 + 15)
            s2 = random.randint(5, 20)
            d2 = s1 + s2 - d1
            c11 = random.randint(4, 15)
            c12 = random.randint(2, 12)
            c21 = random.randint(1, 10)
            c22 = random.randint(3, 15)
            delta = c21 - c22 + c12 - c11
            if delta < 0:
                break

        x11 = d1
        x12 = s1 - d1
        x21 = 0
        x22 = s2
        theta = min(x22, x11)
        new_x21 = x21 + theta
        new_x22 = x22 - theta
        new_x12 = x12 + theta
        new_x11 = x11 - theta

        costs = [c11, c12, c21, c22]
        initial_allocations = [x11, x12, x21, x22]
        final_allocations = [new_x11, new_x12, new_x21, new_x22]
        initial_terms = cost_terms(initial_allocations, costs)
        final_terms = cost_terms(final_allocations, costs)
        initial_sub1 = initial_terms[0] + initial_terms[1]
        initial_sub2 = initial_sub1 + initial_terms[2]
        initial_cost = initial_sub2 + initial_terms[3]
        final_sub1 = final_terms[0] + final_terms[1]
        final_sub2 = final_sub1 + final_terms[2]
        final_cost = final_sub2 + final_terms[3]
        delta_first = c21 - c22
        delta_second = delta_first + c12

        steps = [
            step("TRANSPORT_SETUP", f"supply=({s1},{s2})",
                 f"demand=({d1},{d2})",
                 f"costs=({c11},{c12};{c21},{c22})"),
            step("CHECK", f"{s1}+{s2}", f"{d1}+{d2}", "balanced"),
            step("NW_ALLOC", "cell x11", f"min({s1},{d1})", x11),
            step("S", s1, x11, x12),
            step("NW_ALLOC", "cell x12", "remaining row 1 supply", x12),
            step("NW_ALLOC", "cell x22", "remaining row 2 supply", x22),
            step("NW_ALLOC", allocation_text(x11, x12, x21, x22)),
            step("COST", "initial"),
        ]
        for allocation, cost, term in zip(initial_allocations, costs,
                                          initial_terms):
            steps.append(step("M", allocation, cost, term))
        steps += [
            step("A", initial_terms[0], initial_terms[1], initial_sub1),
            step("A", initial_sub1, initial_terms[2], initial_sub2),
            step("A", initial_sub2, initial_terms[3], initial_cost),
            step("STEPPING_STONE", "enter x21",
                 "+x21 -x22 +x12 -x11"),
            step("S", c21, c22, delta_first),
            step("A", delta_first, c12, delta_second),
            step("S", delta_second, c11, delta),
            step("CHECK", f"delta={delta}", "improves cost"),
            step("THETA", f"min({x22},{x11})", theta),
            step("A", x21, theta, new_x21),
            step("S", x22, theta, new_x22),
            step("A", x12, theta, new_x12),
            step("S", x11, theta, new_x11),
            step("NW_ALLOC", allocation_text(new_x11, new_x12,
                                              new_x21, new_x22)),
            step("COST", "improved"),
        ]
        for allocation, cost, term in zip(final_allocations, costs,
                                          final_terms):
            steps.append(step("M", allocation, cost, term))
        steps += [
            step("A", final_terms[0], final_terms[1], final_sub1),
            step("A", final_sub1, final_terms[2], final_sub2),
            step("A", final_sub2, final_terms[3], final_cost),
        ]
        answer = (
            f"initial cost={initial_cost}; improved "
            f"{allocation_text(new_x11, new_x12, new_x21, new_x22)}; "
            f"final cost={final_cost}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Use northwest-corner then one stepping-stone improvement for "
            f"a 2x2 transportation problem with supply ({s1},{s2}), demand "
            f"({d1},{d2}), and costs [[{c11},{c12}],[{c21},{c22}]]."
        )
        return dict(
            problem_id=jid(),
            operation="transportation_nw_stepping_stone",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
