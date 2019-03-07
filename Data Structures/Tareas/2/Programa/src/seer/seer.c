#include <gtk/gtk.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

/** Size in pixels of our basic grid square */
#define CELL_SIZE 48
/** Space between blocks to separate them */
#define SEPARATION 5

/* Specify the different types of cells
 * EMPTY_TOP is the top cell in an empty vertical pair
 * EMPTY_LEFT is the left cell in an empty horizontal pair
 * MAGNET_TOP_P is the positive top cell in a vertical magnet
 * MAGNET_LEFT_P is the positive top cell in a horizontal magnet
 * MAGNET_TOP_N is the negative top cell in a vertical magnet
 * MAGNET_LEFT_N is the negative top cell in a horizontal magnet
 * PASS is a cell that must no me drawn uppon
 */
typedef enum
{
    EMPTY_TOP,
    EMPTY_LEFT,
    MAGNET_TOP_P,
    MAGNET_LEFT_P,
    MAGNET_TOP_N,
    MAGNET_LEFT_N,
    PASS
} CellType;


pthread_t *update_thread;

/** Width of our matrix */
uint8_t width;
/** Height of our matrix */
uint8_t height;
/** Matrix to keep track of the state of the board */
CellType **board;
/** Array to keep track of left, right, top and bottom numbers */
int *left_array;
int *right_array;
int *top_array;
int *bottom_array;

/** Pointers to images that are the empty spaces */
cairo_surface_t *vertical_empty_sprite;
cairo_surface_t *horizontal_empty_sprite;

/** Pointers to images that are our magnets */
cairo_surface_t *vertical_positive_magnet_sprite;
cairo_surface_t *horizontal_positive_magnet_sprite;
cairo_surface_t *vertical_negative_magnet_sprite;
cairo_surface_t *horizontal_negative_magnet_sprite;

/** Pointers to images that are our plus and minus sign */
cairo_surface_t *plus_sign_sprite;
cairo_surface_t *minus_sign_sprite;

/** Arrays used to store the numbers displayd on the board */
cairo_surface_t **number_sprite;

/** Helper method to draw all the numbers on the edges of the board */
void cairo_draw_numbers(cairo_t *cr)
{
	/** We first draw the vertical numbers */
	for (int row = 0; row < height; row++)
	{
		double pos_x1 = 0;
		double pos_x2 = width * CELL_SIZE + (width + 1) * SEPARATION + CELL_SIZE;
		double pos_y =  (row + 1) * (SEPARATION + CELL_SIZE);
		if (left_array[row] > 0)
		{
			cairo_set_source_surface(cr, number_sprite[left_array[row]], pos_x1, pos_y);
			cairo_paint(cr);
		}
		if (right_array[row] > 0)
		{
			cairo_set_source_surface(cr, number_sprite[right_array[row]], pos_x2, pos_y);
			cairo_paint(cr);
		}
	}
	/** We then draw the horizontal numbers */
	for (int col = 0; col < width; col++)
	{
		double pos_x = (col + 1) * (SEPARATION + CELL_SIZE);
		double pos_y1 = 0;
		double pos_y2 = height * CELL_SIZE + (height + 1) * SEPARATION + CELL_SIZE;
		if (top_array[col] > 0)
		{
			cairo_set_source_surface(cr, number_sprite[top_array[col]], pos_x, pos_y1);
			cairo_paint(cr);
		}
		if (bottom_array[col] > 0)
		{
			cairo_set_source_surface(cr, number_sprite[bottom_array[col]], pos_x, pos_y2);
			cairo_paint(cr);
		}
	}
}

/** Helper method to draw the magnets and empty spaces */
void cairo_draw_cell(cairo_t *cr, CellType cell, int x, int y)
{
	double pos_x = x * CELL_SIZE + (x + 1) * SEPARATION + CELL_SIZE;
	double pos_y = y * CELL_SIZE + (y + 1) * SEPARATION + CELL_SIZE;
	switch (cell)
	{
	case EMPTY_TOP:
		cairo_set_source_surface(cr, vertical_empty_sprite, pos_x, pos_y);
		break;
	case EMPTY_LEFT:
		cairo_set_source_surface(cr, horizontal_empty_sprite, pos_x, pos_y);
		break;
	case MAGNET_TOP_P:
		cairo_set_source_surface(cr, vertical_positive_magnet_sprite, pos_x, pos_y);
		break;
	case MAGNET_LEFT_P:
		cairo_set_source_surface(cr, horizontal_positive_magnet_sprite, pos_x, pos_y);
		break;
	case MAGNET_TOP_N:
		cairo_set_source_surface(cr, vertical_negative_magnet_sprite, pos_x, pos_y);
		break;
	case MAGNET_LEFT_N:
		cairo_set_source_surface(cr, horizontal_negative_magnet_sprite, pos_x, pos_y);
		break;
	case PASS:
		return;
	default:
		return;
	}
	cairo_paint(cr);
}

/** Renders all the elements on the screen */
gboolean draw(GtkWidget *widget, cairo_t *cr, gpointer data)
{
	/* Color of the background is 7C7062 Hex Color | RGB: 124, 112, 98 */
	cairo_set_source_rgb(cr, 124.0 / 255.0, 112.0 / 255.0, 98.0 / 255.0);
	cairo_paint(cr);

	/* We draw the magnets and the empty spaces */
	for (int row = 0; row < height; row++)
	{
		for (int col = 0; col < width; col++)
		{
			cairo_draw_cell(cr, board[row][col], col, row);
		}
	}

	/* We draw the plus and minus sign */
	cairo_set_source_surface(cr, plus_sign_sprite, SEPARATION, SEPARATION);
	cairo_paint(cr);
	cairo_set_source_surface(cr, minus_sign_sprite, (width + 1) * (CELL_SIZE + SEPARATION + 1), (height + 1) * (CELL_SIZE + SEPARATION + 1));
	cairo_paint(cr);

	/* We draw the numbers on the edges */
	cairo_draw_numbers(cr);

	return TRUE;
}
/*
void snapshot(char *filename)
{
	double window_width = (CELL_SIZE + SEPARATION) * width;
	double window_height = (CELL_SIZE + SEPARATION) * height;

	// Imprimimos las imagenes del tablero
	cairo_surface_t *surface;
	cairo_t *cr;

	surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, window_width, window_height);
	cr = cairo_create(surface);

	// Dibuja el estado actual
	draw(NULL, cr, NULL);

	cairo_surface_write_to_png(surface, filename);

	cairo_surface_destroy(surface);
	cairo_destroy(cr);
}
*/

/** Method that recieves STDIN input from solver and updates the board acordingly */
void *update(void *canvas)
{
	uint8_t row, col;
	CellType val;
	char command[16];

	while (true)
	{
		/* We run the program until we recieve an end command or an invalid one */
		if (fscanf(stdin, "%s", command))
		{
			if (!strcmp(command, "END"))
			{
				gtk_main_quit();
				break;
			}
			else if (!strcmp(command, "CELL"))
			{
				if (!fscanf(stdin, "%hhu", &row))
					break;
				if (!fscanf(stdin, "%hhu", &col))
					break;
				if (!fscanf(stdin, "%u", &val))
					break;
				board[row][col] = val;
			}
			else if (!strcmp(command, "NUMBER"))
			{
				if (!fscanf(stdin, "%hhu", &row))
					break;
				if (!fscanf(stdin, "%hhu", &col))
					break;
				if (!fscanf(stdin, "%u", &val))
					break;
				if (row == 0)
					top_array[col] = val;
				else if (row == 1)
					bottom_array[col] = val;
				else if (row == 2)
					left_array[col] = val;
				else if (row == 3)
					right_array[col] = val;
			}
			else if (!strcmp(command, "SNAPSHOT"))
			{
				char filename[64];
				if (!fscanf(stdin, "%s", filename))
					break;
				//snapshot(filename);
			}
			else
			{
				break;
			}
		}
		else
		{
			break;
		}
		gtk_widget_queue_draw(canvas);
	}
	pthread_exit(NULL);
}

/** Initialize the thread that will run the image */
void spawn_updater(GtkWidget *widget, gpointer user_data)
{
	/* Create the thread */
	update_thread = malloc(sizeof(pthread_t));
	/* Execute the thread */
	pthread_create(update_thread, NULL, update, widget);
}

/** Init our board with its default values and assign the pointers */
void matrix_init()
{
	vertical_empty_sprite = cairo_image_surface_create_from_png("assets/empty_vertical.png");
	horizontal_empty_sprite = cairo_image_surface_create_from_png("assets/empty_horizontal.png");
	vertical_positive_magnet_sprite = cairo_image_surface_create_from_png("assets/magnet_positive_vertical.png");
	horizontal_positive_magnet_sprite = cairo_image_surface_create_from_png("assets/magnet_positive_horizontal.png");
	vertical_negative_magnet_sprite = cairo_image_surface_create_from_png("assets/magnet_negative_vertical.png");
	horizontal_negative_magnet_sprite = cairo_image_surface_create_from_png("assets/magnet_negative_horizontal.png");
	number_sprite = malloc(sizeof(cairo_surface_t *) * 10);
	number_sprite[0] = cairo_image_surface_create_from_png("assets/0.png");
	number_sprite[1] = cairo_image_surface_create_from_png("assets/1.png");
	number_sprite[2] = cairo_image_surface_create_from_png("assets/2.png");
	number_sprite[3] = cairo_image_surface_create_from_png("assets/3.png");
	number_sprite[4] = cairo_image_surface_create_from_png("assets/4.png");
	number_sprite[5] = cairo_image_surface_create_from_png("assets/5.png");
	number_sprite[6] = cairo_image_surface_create_from_png("assets/6.png");
	number_sprite[7] = cairo_image_surface_create_from_png("assets/7.png");
	number_sprite[8] = cairo_image_surface_create_from_png("assets/8.png");
	number_sprite[9] = cairo_image_surface_create_from_png("assets/9.png");
	plus_sign_sprite = cairo_image_surface_create_from_png("assets/plus.png");
	minus_sign_sprite = cairo_image_surface_create_from_png("assets/minus.png");

	top_array = malloc(sizeof(int) * width);
	bottom_array = malloc(sizeof(int) * width);
	left_array = malloc(sizeof(int) * height);
	right_array = malloc(sizeof(int) * height);

	for (int row = 0; row < height; row++)
	{
		left_array[row] = -1;
		right_array[row] = -1;
	}
	for (int col = 0; col < width; col++)
	{
		top_array[col] = -1;
		bottom_array[col] = -1;
	}

	board = malloc(sizeof(CellType *) * height);
	for (int row = 0; row < height; row++)
	{
		board[row] = malloc(sizeof(CellType) * width);

		for (int col = 0; col < width; col++)
		{
			board[row][col] = -1;
		}
	}
}
/** Release all our memmory */
void matrix_destroy()
{
	/** Free our spirtes */
	free(vertical_empty_sprite);
	free(horizontal_empty_sprite);
	free(vertical_positive_magnet_sprite);
	free(horizontal_positive_magnet_sprite);
	free(vertical_negative_magnet_sprite);
	free(horizontal_negative_magnet_sprite);
	free(number_sprite);
	free(plus_sign_sprite);
	free(minus_sign_sprite);

	/** Free our arrays for out numbers */
	free(top_array);
	free(bottom_array);
	free(left_array);
	free(right_array);

	for (int row = 0; row < height; row++)
	{
		free(board[row]);
	}
	free(board);
}

bool check_parameters(int argc, char **argv)
{
	if (argc != 3)
		return false;
	return true;
}

/** Visualize the image created by the renderer */
int main(int argc, char **argv)
{
	/* Check that our params are correct */
	if (!check_parameters(argc, argv))
		return 1;

	/* Load the puzzle */
	width = atoi(argv[1]);
	height = atoi(argv[2]);

	matrix_init();

	/* We close the GTK channel so that it doesn't cause trouble */
	fclose(stderr);

	/* Initialize GTK */
	gtk_init(0, NULL);

	/* Create the window */
	GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
	g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

	/* Create the canvas */
	GtkWidget *canvas = gtk_drawing_area_new();

	/* Set dimensions of the Canvas */
	double window_width = (CELL_SIZE + SEPARATION) * width + SEPARATION + 2 * (CELL_SIZE + SEPARATION);
	double window_height = (CELL_SIZE + SEPARATION) * height + SEPARATION + 2 * (CELL_SIZE + SEPARATION);

	gtk_widget_set_size_request(canvas, window_width, window_height);

	/* Link events to the method to our canvas */
	g_signal_connect(canvas, "draw", G_CALLBACK(draw), NULL);
	g_signal_connect(canvas, "realize", G_CALLBACK(spawn_updater), NULL);

	/* Insert the canvas in the window */
	gtk_container_add(GTK_CONTAINER(window), canvas);

	/* Show everything */
	gtk_widget_show(canvas);
	gtk_widget_show(window);

	/* Restart the execution of GTK */
	gtk_main();

	free(update_thread);
	matrix_destroy();

	return 0;
}
