"""The select entities for musiccast."""

from aiomusiccast.capabilities import OptionSetter

from homeassistant.components.select import SelectEntity
from homeassistant.components.yamaha_musiccast import (
    DOMAIN,
    MusicCastCapabilityEntity,
    MusicCastDataUpdateCoordinator,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MusicCast select entities based on a config entry."""
    coordinator: MusicCastDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    select_entities = []

    for capability in coordinator.data.capabilities:
        if isinstance(capability, OptionSetter):
            select_entities.append(SelectableCapapility(coordinator, capability))

    for zone, data in coordinator.data.zones.items():
        for capability in data.capabilities:
            if isinstance(capability, OptionSetter):
                select_entities.append(
                    SelectableCapapility(coordinator, capability, zone)
                )

    async_add_entities(select_entities)


class SelectableCapapility(MusicCastCapabilityEntity, SelectEntity):
    """Representation of a MusicCast Select entity."""

    capability: OptionSetter

    async def async_select_option(self, option: str) -> None:
        """Select the given option."""
        value = {val: key for key, val in self.capability.options.items()}[option]
        await self.capability.set(value)

    @property
    def device_class(self) -> str:
        """Return the ID of the capability, to identify the entity for translations."""
        return f"{DOMAIN}__{self.capability.id.lower()}"

    @property
    def options(self):
        """Return the list possible options."""
        return list(self.capability.options.values())

    @property
    def current_option(self):
        """Return the currently selected option."""
        return self.capability.options[self.capability.current]