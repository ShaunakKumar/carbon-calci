from flask import Flask, render_template, request

app = Flask(__name__)

# ======================
# EMISSION FACTORS
# ======================
ELECTRICITY = 0.82
SOLAR = 0.82
LPG = 14.2
GENERATOR = 2.5
INVERTER = 0.6

AC = 1.6
FAN = 0.075
FRIDGE = 1.2
TV = 0.1
WASHING = 0.6

PETROL = 2.31
DIESEL = 2.68
BUS = 0.089
TRAIN = 0.041

SHORT_FLIGHT = 0.15
LONG_FLIGHT = 0.11

WATER = 0.0003
WASTE = 0.5
PAPER = 0.005
CLOTHES = 6
ONLINE = 1.8

VEG = 50
NON_VEG = 120

INTERNET = 0.06
MOBILE = 0.005
LAPTOP = 0.02
ELEVATOR = 0.015

TREE_OFFSET = 21


# ======================
# MAIN PAGE
# ======================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            # ---------- ENERGY ----------
            electricity = float(request.form.get("electricity") or 0)
            solar = float(request.form.get("solar_units") or 0)
            lpg = float(request.form.get("lpg") or 0)
            generator = float(request.form.get("generator_liters") or 0)
            inverter = float(request.form.get("inverter_units") or 0)

            energy = (
                electricity * ELECTRICITY +
                lpg * LPG +
                generator * GENERATOR +
                inverter * INVERTER -
                solar * SOLAR
            )

            # ---------- APPLIANCES ----------
            ac = float(request.form.get("ac_hours") or 0)
            fan = float(request.form.get("fan_hours") or 0)
            fridge = float(request.form.get("fridge_days") or 0)
            tv = float(request.form.get("tv_hours") or 0)
            washing = float(request.form.get("washing_cycles") or 0)

            appliances = (
                ac * AC +
                fan * FAN +
                fridge * FRIDGE +
                tv * TV +
                washing * WASHING
            )

            # ---------- TRANSPORT ----------
            fuel_type = request.form.get("fuel_type")
            fuel_liters = float(request.form.get("fuel_liters") or 0)

            if fuel_type == "petrol":
                fuel = fuel_liters * PETROL
            else:
                fuel = fuel_liters * DIESEL

            bus = float(request.form.get("bus_km") or 0)
            train = float(request.form.get("train_km") or 0)

            transport = fuel + (bus * BUS) + (train * TRAIN)

            # ---------- FLIGHTS ----------
            short_flight = float(request.form.get("short_flight_km") or 0)
            long_flight = float(request.form.get("long_flight_km") or 0)

            flights = (short_flight * SHORT_FLIGHT) + (long_flight * LONG_FLIGHT)

            # ---------- LIFESTYLE ----------
            food_type = request.form.get("food_type")
            food = VEG if food_type == "veg" else NON_VEG

            water = float(request.form.get("water_liters") or 0)
            waste = float(request.form.get("waste_kg") or 0)
            paper = float(request.form.get("paper_sheets") or 0)
            clothes = float(request.form.get("clothes_bought") or 0)
            online = float(request.form.get("online_orders") or 0)

            lifestyle = (
                food +
                water * WATER +
                waste * WASTE +
                paper * PAPER +
                clothes * CLOTHES +
                online * ONLINE
            )

            # ---------- DIGITAL ----------
            internet = float(request.form.get("internet_gb") or 0)
            mobile = float(request.form.get("mobile_hours") or 0)
            laptop = float(request.form.get("laptop_hours") or 0)
            elevator = float(request.form.get("elevator_trips") or 0)

            digital = (
                internet * INTERNET +
                mobile * MOBILE +
                laptop * LAPTOP +
                elevator * ELEVATOR
            )

            # ---------- TOTAL ----------
            total = energy + appliances + transport + flights + lifestyle + digital

            # ---------- OFFSET ----------
            trees = float(request.form.get("trees_planted") or 0)
            offset = (trees * TREE_OFFSET) / 12

            net = total - offset

            # ---------- IMPACT ----------
            if net < 300:
                level = "LOW"
            elif net < 750:
                level = "MEDIUM"
            else:
                level = "HIGH"

            result = {
                "total": round(total, 2),
                "offset": round(offset, 2),
                "net": round(net, 2),
                "level": level
            }
        except Exception:
            app.logger.exception("Exception while processing / request")
            raise

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
