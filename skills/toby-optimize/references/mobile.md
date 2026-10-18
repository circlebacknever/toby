# Mobile (React Native, with notes for native)

This file covers lists, images, and bridge calls in React Native. Open it when a mobile screen is slow.

## Lists

Use `FlatList` for every list that can grow, because it costs the same to write as `ScrollView` and renders only the visible rows. Move to `FlashList` when measured scrolling drops frames on a large or image-heavy list. Keep `ScrollView` for a small, fixed set of differently built sections, such as a settings screen. Always pass a stable id as the key, define `renderItem` outside the render function, set explicit image sizes, and set `scrollEventThrottle={16}` for scroll-driven animation.

## Images

Request an image at the size the screen draws it. A 4 MB photo decodes to tens of megabytes for a 40 px avatar, so 50 of them crash the app. Ask the server or CDN for an 80 px thumbnail, and pair long image lists with `expo-image` or `react-native-fast-image`.

## Bridge calls

Each JS-to-native call costs a few milliseconds, so a loop of 500 `getContact(id)` calls takes seconds. Add one native method that returns the whole list, even under React Native's New Architecture.
