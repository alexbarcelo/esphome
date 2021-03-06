import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, spi
from esphome.const import CONF_ID, CONF_MAINS_FILTER, ICON_THERMOMETER, UNIT_CELSIUS

max31856_ns = cg.esphome_ns.namespace('max31856')
MAX31856Sensor = max31856_ns.class_('MAX31856Sensor', sensor.Sensor, cg.PollingComponent,
                                    spi.SPIDevice)

MAX31865ConfigFilter = max31856_ns.enum('MAX31856ConfigFilter')
FILTER = {
    '50HZ': MAX31865ConfigFilter.FILTER_50HZ,
    '60HZ': MAX31865ConfigFilter.FILTER_60HZ,
}

CONFIG_SCHEMA = sensor.sensor_schema(UNIT_CELSIUS, ICON_THERMOMETER, 1).extend({
    cv.GenerateID(): cv.declare_id(MAX31856Sensor),
    cv.Optional(CONF_MAINS_FILTER, default='60HZ'): cv.enum(FILTER, upper=True, space=''),
}).extend(cv.polling_component_schema('60s')).extend(spi.SPI_DEVICE_SCHEMA)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield spi.register_spi_device(var, config)
    yield sensor.register_sensor(var, config)
    cg.add(var.set_filter(config[CONF_MAINS_FILTER]))
