def transfrom(self, x, y):
    return self.transfrom_3D(x, y)
    #return self.transfrom_2D(x, y)


def transfrom_2D(self, x, y):
    return int(x), int(y)


def transfrom_3D(self, x, y):
    line_y = y + self.perspective_point_y / self.height
    if line_y > self.perspective_point_y:
        line_y = self.perspective_point_y

    diff_x = x - self.perspective_point_x
    diff_y = self.perspective_point_y - line_y
    factor_y = diff_y / self.perspective_point_y
    factor_y = pow(factor_y, 2)

    tr_x = self.perspective_point_x + diff_x * factor_y
    tr_y = self.perspective_point_y - factor_y * self.perspective_point_y
    return int(tr_x), int(tr_y)
