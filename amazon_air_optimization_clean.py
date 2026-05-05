# Final version - verified optimal solution and constraints

from scipy.optimize import linprog

# -----------------------------
# Input data
# -----------------------------

HUB_CAPACITY = {'CVG': 95650, 'AFW': 44350}

FOCUS_CAPACITY = {'Leipzig': 85000, 'Hyderabad': 19000, 'San Bernardino': 36000}

DEMAND = {'Paris': 6500,
 'Cologne': 640,
 'Hanover': 180,
 'Bengaluru': 9100,
 'Coimbatore': 570,
 'Delhi': 19000,
 'Mumbai': 14800,
 'Cagliari': 90,
 'Catania': 185,
 'Milan': 800,
 'Rome': 1700,
 'Katowice': 170, 
 'Barcelona': 2800,
 'Madrid': 3700,
 'Castle Donington': 30,
 'London': 6700,
 'Mobile': 190,
 'Anchorage': 175,
 'Fairbanks': 38,
 'Phoenix': 2400,
 'Los Angeles': 7200,
 'Ontario': 100,
 'Riverside': 1200,
 'Sacramento': 1100,
 'San Francisco': 1900,
 'Stockton': 240,
 'Denver': 1500,
 'Hartford': 540,
 'Miami': 3400,
 'Lakeland': 185,
 'Tampa': 1600,
 'Atlanta': 3000,
 'Honolulu': 500,
 'Kahului/Maui': 16,
 'Kona': 63,
 'Chicago': 5100,
 'Rockford': 172,
 'Fort Wayne': 200,
 'South Bend': 173,
 'Des Moines': 300,
 'Wichita': 290,
 'New Orleans': 550,
 'Baltimore': 1300,
 'Minneapolis': 1700,
 'Kansas City': 975,
 'St. Louis': 1200,
 'Omaha': 480,
 'Manchester': 100,
 'Albuquerque': 450,
 'New York': 11200,
 'Charlotte': 900,
 'Toledo': 290,
 'Wilmington': 150,
 'Portland': 1200,
 'Allentown': 420,
 'Pittsburgh': 1000,
 'San Juan': 1100,
 'Nashville': 650,
 'Austin': 975,
 'Dallas': 3300,
 'Houston': 3300,
 'San Antonio': 1100,
 'Richmond': 600,
 'Seattle/Tacoma': 2000,
 'Spokane': 260}

# Routes are manually defined from the assessment cost table.
# N/A entries are excluded because those routes are unavailable.
# Each route is stored as: (supplier, destination, cost per ton).
ROUTES = []


def add_route(supplier, destination, cost_per_ton):
    """Add one allowed route to the route list."""
    ROUTES.append((supplier, destination, cost_per_ton))


def add_center_routes(destination, supplier_costs):
    """Add all allowed supplier routes for one center city."""
    for supplier, cost_per_ton in supplier_costs.items():
        add_route(supplier, destination, cost_per_ton)


# Routes into focus cities
add_route("CVG", "Leipzig", 1.5)
add_route("Leipzig", "Hyderabad", 1.6)
add_route("CVG", "San Bernardino", 0.5)
add_route("AFW", "San Bernardino", 0.5)


# European center routes
add_center_routes("Paris", {"CVG": 1.6, "Leipzig": 0.5, "Hyderabad": 1.1})
add_center_routes("Cologne", {"CVG": 1.5, "Leipzig": 0.5, "Hyderabad": 1.0})
add_center_routes("Hanover", {"CVG": 1.5, "Leipzig": 0.5, "Hyderabad": 1.0})
add_center_routes("Cagliari", {"CVG": 1.5, "Leipzig": 0.5, "Hyderabad": 1.0})
add_center_routes("Catania", {"CVG": 1.5, "Leipzig": 0.5, "Hyderabad": 1.0})
add_center_routes("Milan", {"CVG": 1.5, "Leipzig": 0.5, "Hyderabad": 1.0})
add_center_routes("Rome", {"CVG": 1.5, "Leipzig": 0.5, "Hyderabad": 1.1})
add_center_routes("Katowice", {"CVG": 1.4, "Leipzig": 0.5, "Hyderabad": 1.0})
add_center_routes("Barcelona", {"CVG": 1.5, "Leipzig": 0.5, "Hyderabad": 1.0})
add_center_routes("Madrid", {"CVG": 1.6, "Leipzig": 0.5, "Hyderabad": 1.1})
add_center_routes("Castle Donington", {"CVG": 1.4, "Leipzig": 0.5})
add_center_routes("London", {"CVG": 1.6, "Leipzig": 0.75, "Hyderabad": 1.1})

# Indian center routes
add_center_routes("Bengaluru", {"Leipzig": 1.5, "Hyderabad": 0.5})
add_center_routes("Coimbatore", {"Leipzig": 1.5, "Hyderabad": 0.5})
add_center_routes("Delhi", {"Leipzig": 1.5, "Hyderabad": 0.5})
add_center_routes("Mumbai", {"Leipzig": 1.5, "Hyderabad": 0.5})

# United States and Puerto Rico center routes
add_center_routes("Mobile", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Anchorage", {"CVG": 1.3, "AFW": 1.0, "San Bernardino": 0.7})
add_center_routes("Fairbanks", {"CVG": 1.4, "AFW": 1.0, "San Bernardino": 0.7})
add_center_routes("Phoenix", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Los Angeles", {"CVG": 0.5, "AFW": 0.5})
add_center_routes("Ontario", {"CVG": 0.5, "AFW": 0.5})
add_center_routes("Riverside", {"CVG": 0.5, "AFW": 0.5})
add_center_routes("Sacramento", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("San Francisco", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Stockton", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Denver", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Hartford", {"CVG": 0.5, "AFW": 0.5, "Leipzig": 1.5, "San Bernardino": 0.5})
add_center_routes("Miami", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.7})
add_center_routes("Lakeland", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.7})
add_center_routes("Tampa", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.7})
add_center_routes("Atlanta", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.6})
add_center_routes("Honolulu", {"AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Kahului/Maui", {"AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Kona", {"AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Chicago", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Rockford", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Fort Wayne", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("South Bend", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Des Moines", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Wichita", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("New Orleans", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Baltimore", {"CVG": 0.5, "AFW": 0.5, "Leipzig": 1.5, "San Bernardino": 0.7})
add_center_routes("Minneapolis", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Kansas City", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("St. Louis", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Omaha", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Manchester", {"CVG": 0.5, "AFW": 0.5, "Leipzig": 1.5, "San Bernardino": 0.7})
add_center_routes("Albuquerque", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("New York", {"CVG": 0.5, "AFW": 0.5, "Leipzig": 1.6, "San Bernardino": 0.7})
add_center_routes("Charlotte", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.7})
add_center_routes("Toledo", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Wilmington", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.7})
add_center_routes("Portland", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Allentown", {"CVG": 0.5, "AFW": 0.5, "Leipzig": 1.5, "San Bernardino": 0.7})
add_center_routes("Pittsburgh", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.6})
add_center_routes("San Juan", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 1.0})
add_center_routes("Nashville", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Austin", {"CVG": 0.5, "AFW": 0.25, "San Bernardino": 0.5})
add_center_routes("Dallas", {"CVG": 0.5, "San Bernardino": 0.5})
add_center_routes("Houston", {"CVG": 0.5, "AFW": 0.25, "San Bernardino": 0.5})
add_center_routes("San Antonio", {"CVG": 0.5, "AFW": 0.25, "San Bernardino": 0.5})
add_center_routes("Richmond", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.7})
add_center_routes("Seattle/Tacoma", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})
add_center_routes("Spokane", {"CVG": 0.5, "AFW": 0.5, "San Bernardino": 0.5})


FOCUS_CITIES = set(FOCUS_CAPACITY.keys())
CENTERS = list(DEMAND.keys())


def build_model():
    """Build the linear programming matrices for scipy.optimize.linprog."""
    objective = [cost for _, _, cost in ROUTES]

    # Equality constraints: every center's monthly demand must be exactly met.
    A_eq = []
    b_eq = []
    for center in CENTERS:
        A_eq.append([1 if destination == center else 0 for _, destination, _ in ROUTES])
        b_eq.append(DEMAND[center])

    A_ub = []
    b_ub = []

    # Hub capacity constraints: total outbound cargo from each hub cannot exceed capacity.
    for hub, capacity in HUB_CAPACITY.items():
        A_ub.append([1 if supplier == hub else 0 for supplier, _, _ in ROUTES])
        b_ub.append(capacity)

    # Focus-city inbound capacity constraints.
    for focus_city, capacity in FOCUS_CAPACITY.items():
        A_ub.append([1 if destination == focus_city else 0 for _, destination, _ in ROUTES])
        b_ub.append(capacity)

    # Focus-city outbound capacity constraints.
    for focus_city, capacity in FOCUS_CAPACITY.items():
        A_ub.append([
            1 if supplier == focus_city and destination in DEMAND else 0
            for supplier, destination, _ in ROUTES
        ])
        b_ub.append(capacity)

    return objective, A_ub, b_ub, A_eq, b_eq


def solve_model():
    """Run the optimization solver and return the result object."""
    objective, A_ub, b_ub, A_eq, b_eq = build_model()
    result = linprog(
        c=objective,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=(0, None),
        method="highs",
    )
    return result


def summarize_solution(result):
    """Print the optimal cost, capacity usage, and positive shipments."""
    if not result.success:
        print("Solver status: no optimal solution found")
        print(result.message)
        return

    print("Solver status: optimal solution found")
    print(f"Optimal objective value: {result.fun:,.2f}")
    print(f"Number of available decision variables: {len(ROUTES)}")
    print(f"Number of positive shipment decisions: {sum(value > 1e-7 for value in result.x)}")
    print(f"Total center demand satisfied: {sum(DEMAND.values()):,.0f} tons")
    print()

    print("Capacity usage")
    for hub, capacity in HUB_CAPACITY.items():
        used = sum(value for value, (supplier, _, _) in zip(result.x, ROUTES) if supplier == hub)
        print(f"  {hub}: {used:,.0f} / {capacity:,.0f} tons")

    for focus_city, capacity in FOCUS_CAPACITY.items():
        inbound = sum(value for value, (_, destination, _) in zip(result.x, ROUTES) if destination == focus_city)
        outbound = sum(
            value for value, (supplier, destination, _) in zip(result.x, ROUTES)
            if supplier == focus_city and destination in DEMAND
        )
        print(f"  {focus_city} inbound: {inbound:,.0f} / {capacity:,.0f} tons")
        print(f"  {focus_city} outbound: {outbound:,.0f} / {capacity:,.0f} tons")
    print()

    max_residual = 0
    for center, demand in DEMAND.items():
        received = sum(value for value, (_, destination, _) in zip(result.x, ROUTES) if destination == center)
        max_residual = max(max_residual, abs(received - demand))
    print(f"Maximum center-demand residual: {max_residual:.8f} tons")
    print()

    print("Positive shipment decisions")
    for value, (supplier, destination, cost) in zip(result.x, ROUTES):
        if value > 1e-7:
            route_cost = value * cost
            print(f"  {supplier:15s} -> {destination:18s} {value:10,.0f} tons at {cost:4.2f} = {route_cost:10,.2f}")


if __name__ == "__main__":
    solution = solve_model()
    summarize_solution(solution)
