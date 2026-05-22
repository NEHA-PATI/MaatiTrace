export function getResolutionFromZoom(
  zoom
) {

  if (zoom <= 5) return 5;

  if (zoom <= 7) return 6;

  if (zoom <= 9) return 7;

  if (zoom <= 11) return 8;

  return 9;
}