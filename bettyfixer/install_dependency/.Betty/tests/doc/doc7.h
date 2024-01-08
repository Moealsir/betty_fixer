#ifndef _DOC6_H_
#define _DOC6_H_

/**
 * struct dog - A Dog structure
 *
 * @name: Name
 * @age: Test
 */
struct dog
{
	char *name;
	float age;
	char *owner;
};

/**
 * enum test - Test
 *
 * @SECOND: Second
 * @THIRD: Third
 */
enum test
{
	FIRST = 0,
	SECOND,
	THIRD
};

/**
 * union color - Color
 *
 * @value: Value
 */
union color
{
	char rgba[4];
	unsigned int value;
};

/**
 * struct animal - Animal
 *
 * @name: The name
 * @color: color
 */
typedef struct animal
{
	char *name;
	enum test race;
	union color color;
} t_animal;

/**
 * enum test2 - Test
 *
 * @FIRST: First
 * @THIRD: Third
 */
enum test2
{
	FIRST = 0,
	SECOND,
	THIRD
};

/**
 * union color2 - Color
 *
 * @rgba: RGBA
 */
typedef union color2
{
	char rgba[4];
	unsigned int value;
} u_color;

/* No doc is required for func prototypes */
void init_dog(struct dog *d, char *name, float age, char *owner);
void print_dog(struct dog *d);

#endif /* _DOC6_H_ *?
