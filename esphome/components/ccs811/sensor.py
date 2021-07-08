import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_EMPTY,
    ICON_RADIATOR,
    ICON_RESTART,
    STATE_CLASS_MEASUREMENT,
    UNIT_PARTS_PER_MILLION,
    UNIT_PARTS_PER_BILLION,
    CONF_BASELINE,
    CONF_ECO2,
    UNIT_EMPTY,
    CONF_TEMPERATURE,
    CONF_TVOC,
    CONF_HUMIDITY,
    CONF_VERSION,
    ICON_MOLECULE_CO2,
)

DEPENDENCIES = ["i2c"]

ccs811_ns = cg.esphome_ns.namespace("ccs811")
CCS811Component = ccs811_ns.class_(
    "CCS811Component", cg.PollingComponent, i2c.I2CDevice
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(CCS811Component),
            cv.Required(CONF_ECO2): sensor.sensor_schema(
                UNIT_PARTS_PER_MILLION,
                ICON_MOLECULE_CO2,
                0,
                DEVICE_CLASS_EMPTY,
                STATE_CLASS_MEASUREMENT,
            ),
            cv.Required(CONF_TVOC): sensor.sensor_schema(
                UNIT_PARTS_PER_BILLION,
                ICON_RADIATOR,
                0,
                DEVICE_CLASS_EMPTY,
                STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_VERSION): sensor.sensor_schema(
                UNIT_EMPTY,
                ICON_RESTART,
                0,
                DEVICE_CLASS_EMPTY,
                STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_BASELINE): cv.hex_uint16_t,
            cv.Optional(CONF_TEMPERATURE): cv.use_id(sensor.Sensor),
            cv.Optional(CONF_HUMIDITY): cv.use_id(sensor.Sensor),
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(i2c.i2c_device_schema(0x5A))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    sens = await sensor.new_sensor(config[CONF_ECO2])
    cg.add(var.set_co2(sens))
    sens = await sensor.new_sensor(config[CONF_TVOC])
    cg.add(var.set_tvoc(sens))
    if CONF_VERSION in config:
        sens = await sensor.new_sensor(config[CONF_VERSION])
        cg.add(var.set_version(sens))

    if CONF_BASELINE in config:
        cg.add(var.set_baseline(config[CONF_BASELINE]))

    if CONF_TEMPERATURE in config:
        sens = await cg.get_variable(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature(sens))
    if CONF_HUMIDITY in config:
        sens = await cg.get_variable(config[CONF_HUMIDITY])
        cg.add(var.set_humidity(sens))
