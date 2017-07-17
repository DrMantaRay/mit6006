import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def adjacent(self, x, y):
        pixel_list = list()
        pixel_list.append((x, y+1))
        if x < self.width -1:
            pixel_list.append((x+1, y+1))
        if x > 0:
            pixel_list.append((x-1, y+1))
        return pixel_list

    def best_seam(self):
        cur_row = 0
        pixel_energy_dict = {}
        pixel_parent_dict = {}
        for pixel_col_num in range(0, self.width):
            pixel_energy_dict[(pixel_col_num, cur_row)] = self.energy(pixel_col_num, cur_row)
        while cur_row < self.height -1:
            for pixel_col_num in range(0, self.width):
                for adj_pixel in self.adjacent(pixel_col_num, cur_row):
                    if adj_pixel in pixel_energy_dict:
                        if pixel_energy_dict[(pixel_col_num, cur_row)] + self.energy(adj_pixel[0],
                                adj_pixel[1]) < pixel_energy_dict[adj_pixel]:
                            pixel_energy_dict[adj_pixel] = pixel_energy_dict[(pixel_col_num, cur_row)] \
                                                           + self.energy(adj_pixel[0], adj_pixel[1])
                            pixel_parent_dict[adj_pixel] = (pixel_col_num, cur_row)
                    else:
                        pixel_energy_dict[adj_pixel] = pixel_energy_dict[(pixel_col_num, cur_row)] \
                                                       + self.energy(adj_pixel[0], adj_pixel[1])
                        pixel_parent_dict[adj_pixel] = (pixel_col_num, cur_row)
            cur_row +=1

        min_pixel_energy = pixel_energy_dict[(0, self.height - 1)]
        min_pixel_pair = (0, self.height - 1)
        for pixel_col_num in range(0, self.width):
            if pixel_energy_dict[(pixel_col_num, self.height - 1)] < min_pixel_energy:
                min_pixel_energy = pixel_energy_dict[(pixel_col_num, self.height - 1)]
                min_pixel_pair = (pixel_col_num, self.height - 1)

        cur_pixel = min_pixel_pair
        output_list = [cur_pixel]
        while cur_pixel in pixel_parent_dict:
            output_list.append(pixel_parent_dict[cur_pixel])
            cur_pixel = pixel_parent_dict[cur_pixel]
        output_list.reverse()
        return output_list

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
